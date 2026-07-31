function canonicalizeResults(searchRoot)
    % Make results MAT-files byte-reproducible across runs.
    %
    % Two run-to-run differences are neutralised so that byte-identical
    % results stop churning in git/LFS:
    %   1. oo_.time - Dynare's per-model compute time (a timing measurement)
    %      is set to 0 and the file re-saved.
    %   2. The 116-byte text header carries a "Created on: <timestamp>" that
    %      MATLAB rewrites on every save; it is overwritten with a fixed
    %      canonical string. The binary data and the version/endianness bytes
    %      (offsets 116-127) are left untouched, so the files still load.
    %
    % IMPORTANT: run this in its OWN clean MATLAB process, never as a direct
    % call from a Dynare-loaded session. When Dynare is on the path / its
    % globals are live, `save` serialises function-handle workspaces into the
    % MAT subsystem block, producing different bytes for identical data. A
    % clean process (project root on the path, Dynare NOT loaded) strips them
    % deterministically. runModel.m spawns such a child process automatically
    % at the end via utils.subroutines.spawnCanonicalize; to run a full
    % sweep standalone:
    %   matlab -batch "addpath('<project_root>'); utils.subroutines.canonicalizeResults()"
    %
    % Inputs:
    %   searchRoot - folder to scan recursively (string). Defaults to the
    %                project's `models` directory.

    if nargin < 1 || isempty(searchRoot)
        utils.call.paths;   % defines project_path
        searchRoot = fullfile(project_path, 'models');
    end

    % Fixed 116-byte text header (space-padded, no timestamp).
    canon = uint8(repmat(' ', 1, 116));
    text  = uint8('MATLAB 5.0 MAT-file, Platform: MACA64, Created on: (canonicalized)');
    n = min(numel(text), 116);
    canon(1:n) = text(1:n);

    files = dir(fullfile(searchRoot, '**', 'Output', '*_results.mat'));

    nChanged = 0;
    for k = 1:numel(files)
        fpath = fullfile(files(k).folder, files(k).name);
        changed = false;

        % 1. Zero Dynare's per-model timing and always re-save. Re-saving
        %    in a clean session also strips any subsystem bloat written by
        %    a Dynare-loaded session.
        S = load(fpath);
        if isfield(S, 'oo_') && isfield(S.oo_, 'time')
            S.oo_.time = 0;
        end
        save(fpath, '-struct', 'S', '-v7');
        changed = true;

        % 2. Canonicalize the text header (also fixes the fresh timestamp
        %    written by the save above).
        fid = fopen(fpath, 'r+');   % read/write in place, do not truncate
        if fid < 0
            warning('canonicalizeResults:open', 'Could not open %s', fpath);
            continue;
        end
        existing = fread(fid, 116, '*uint8')';
        if ~isequal(existing, canon)
            fseek(fid, 0, 'bof');
            fwrite(fid, canon, 'uint8');
            changed = true;
        end
        fclose(fid);

        nChanged = nChanged + changed;
    end

    fprintf('canonicalizeResults: normalized %d of %d results file(s).\n', ...
            nChanged, numel(files));
end

function spawnCanonicalize(modelName)
    % Canonicalize results for one model (or all models) in a clean child
    % MATLAB process, spawned synchronously via system().
    %
    % Must be a separate process, not a direct call: with Dynare loaded in
    % the calling session, save() writes nondeterministic function-handle
    % context into the MAT subsystem and the bytes differ run-to-run even
    % for identical data. See canonicalizeResults.m.
    %
    % Inputs:
    %   modelName - model folder name under models/ (string). Omit to sweep
    %               the whole models tree.

    utils.call.paths;   % defines project_path

    if nargin < 1 || isempty(modelName)
        modelName  = 'all models';
        searchRoot = '';
    else
        searchRoot = fullfile(project_path, 'models', modelName);
    end

    matlabBin = fullfile(matlabroot, 'bin', 'matlab');
    cmd = sprintf('"%s" -batch "addpath(''%s''); utils.subroutines.canonicalizeResults(''%s'')"', ...
            matlabBin, project_path, searchRoot);
    status = system(cmd);
    if status ~= 0
        warning('spawnCanonicalize:failed', ...
                'canonicalizeResults child process failed (exit %d) for %s.', ...
                status, modelName);
    end
end

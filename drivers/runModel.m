close all;
clear all;
clc;

utils.call.paths;
cd(fullfile(project_path, 'models'));

% Each row specifies a model name, country-group calibration, efficiency-gap
% calibration, and the complete set of deterministic policy paths.
modelList = {
    % Advanced-economy expenditure reallocations.
    'Model_HumanCapital_epsi_ig',          'AE', 'AE',     {{'epsi_igi', 'const', 0.01,  '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsi_cge',         'AE', 'AE',     {{'epsi_ige', 'const', 0.01,  '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsi_cgrd',        'AE', 'AE',     {{'epsi_grd', 'const', 0.01,  '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsi_cgeCgrd',     'AE', 'AE',     {{'epsi_ige', 'const', 0.005, '1:1000'}; {'epsi_grd', 'const', 0.005, '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}

    % Advanced-economy reallocations combined with gradual gap closure.
    'Model_HumanCapital_epsi_igeff25y',    'AE', 'AE',     {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_effgi', 'ramp', 0.359, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsi_cgeeff25y',   'AE', 'AE',     {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_effge', 'ramp', 0.306, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsi_cgrd_eff25y', 'AE', 'AE',     {{'epsi_grd', 'const', 0.01, '1:1000'}; {'epsi_effgrd', 'ramp', 0.399, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}

    % Advanced-economy technology-diffusion variants of the 50/50 mix.
    'Model_HumanCapital_epsicgrd_cge_adt', 'AE', 'AE',     {{'epsi_grd', 'const', 0.005, '1:1000'}; {'epsi_ige', 'const', 0.005, '1:1000'}; {'epsi_q', 'ramp', 0.03, '1:40'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'Model_HumanCapital_epsicgrd_cge_limt','AE', 'AE',     {{'epsi_grd', 'const', 0.005, '1:1000'}; {'epsi_ige', 'const', 0.005, '1:1000'}; {'epsi_q', 'ramp', -0.03, '1:40'}; {'epsi_gc', 'const', -0.01, '1:1000'}}

    % EMDE reallocations under calibrated and 10-percentage-point-higher gaps.
    'EM_Model_HumanCapital_epsiig',        'EM', 'EMnorm', {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsiiglow',     'EM', 'EMlow',  {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicge',       'EM', 'EMnorm', {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicgelow',    'EM', 'EMlow',  {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_gc', 'const', -0.01, '1:1000'}}

    % EMDE 15- and 25-year efficiency reforms. Higher-gap variants close the
    % same number of percentage points and therefore retain a 10 percent gap.
    'EM_Model_HumanCapital_epsiigeff30y',       'EM', 'EMnorm', {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_effgi', 'ramp', 0.406, '1:60'};  {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsiigeff30ylow',    'EM', 'EMlow',  {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_effgi', 'ramp', 0.406, '1:60'};  {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsiigeff25y',       'EM', 'EMnorm', {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_effgi', 'ramp', 0.406, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsiigeff25ylow',    'EM', 'EMlow',  {{'epsi_igi', 'const', 0.01, '1:1000'}; {'epsi_effgi', 'ramp', 0.406, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicgeeff30y',      'EM', 'EMnorm', {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_effge', 'ramp', 0.329, '1:60'};  {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicgeeff30ylow',   'EM', 'EMlow',  {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_effge', 'ramp', 0.329, '1:60'};  {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicgeeff25y',      'EM', 'EMnorm', {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_effge', 'ramp', 0.329, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
    'EM_Model_HumanCapital_epsicgeeff25ylow',   'EM', 'EMlow',  {{'epsi_ige', 'const', 0.01, '1:1000'}; {'epsi_effge', 'ramp', 0.329, '1:100'}; {'epsi_gc', 'const', -0.01, '1:1000'}}
};

modelFilter = getenv('MODEL_FILTER');
if ~isempty(modelFilter)
    modelList = modelList(contains(modelList(:, 1), modelFilter), :);
end

for iModel = 1:size(modelList, 1)
    modelName = modelList{iModel, 1};
    parameterSet = modelList{iModel, 2};
    efficiencySet = modelList{iModel, 3};
    shockSpecs = modelList{iModel, 4};
    shockSpecs{end + 1} = {'eTaux', 'const', 1, '1:2000'};

    utils.subroutines.generateShocksFile([modelName '.shockValues'], shockSpecs);
    copyfile('modelTemplate.mod', [modelName '.mod']);
    copyfile('modelTemplate_steadystate.m', [modelName '_steadystate.m']);

    dynare([modelName '.mod'], 'savemacro', 'json=compute', ...
        sprintf('-DparamFile="%s_parameters.macro"', parameterSet), ...
        sprintf('-DeffFile="%s_efficiency.macro"', efficiencySet), ...
        sprintf('-DshockFile="%s.shockValues"', modelName));
end

utils.subroutines.spawnCanonicalize();

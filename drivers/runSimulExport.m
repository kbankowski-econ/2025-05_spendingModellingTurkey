clear all;
close all;
clc;

utils.call.paths;

modelList = [
    "Model_HumanCapital_epsi_ig"
    "Model_HumanCapital_epsi_cge"
    "Model_HumanCapital_epsi_cgrd"
    "Model_HumanCapital_epsi_cgeCgrd"
    "Model_HumanCapital_epsi_igeff25y"
    "Model_HumanCapital_epsi_cgeeff25y"
    "Model_HumanCapital_epsi_cgrd_eff25y"
    "Model_HumanCapital_epsicgrd_cge_adt"
    "Model_HumanCapital_epsicgrd_cge_limt"
    "EM_Model_HumanCapital_epsiig"
    "EM_Model_HumanCapital_epsiiglow"
    "EM_Model_HumanCapital_epsicge"
    "EM_Model_HumanCapital_epsicgelow"
    "EM_Model_HumanCapital_epsiigeff30y"
    "EM_Model_HumanCapital_epsiigeff30ylow"
    "EM_Model_HumanCapital_epsiigeff25y"
    "EM_Model_HumanCapital_epsiigeff25ylow"
    "EM_Model_HumanCapital_epsicgeeff30y"
    "EM_Model_HumanCapital_epsicgeeff30ylow"
    "EM_Model_HumanCapital_epsicgeeff25y"
    "EM_Model_HumanCapital_epsicgeeff25ylow"
];

output = struct();
for modelName = modelList.'
    resultFile = fullfile(project_path, 'models', modelName, 'Output', ...
        modelName + "_results.mat");
    result = load(resultFile);
    variableIndex = find(strcmp(result.M_.endo_names, 'yd'), 1);
    assert(~isempty(variableIndex), 'Output variable yd is missing from %s.', modelName);

    dataRange = qq(0, 4):qq(0, 4) + size(result.oo_.endo_simul, 2) - 1;
    outputPath = result.oo_.endo_simul(variableIndex, :);
    steadyState = result.oo_.steady_state(variableIndex);
    output.(modelName + "___yd") = Series(dataRange, ...
        (outputPath / steadyState - 1) * 100);
end

output = databank.redate(output, qq(25, 4), qq(2050, 1));
annualOutput = databank.apply(output, ...
    @(x) convert(x, Frequency.YEARLY, "Method", "first"));

dataDir = fullfile(project_path, 'data');
if ~exist(dataDir, 'dir')
    mkdir(dataDir);
end
databank.toCSV(annualOutput, ...
    fullfile(dataDir, 'figure13_yearly.csv'), ...
    yy(2025):yy(2050), ...
    "Decimals", 3, "Comments", false, "Class", false);

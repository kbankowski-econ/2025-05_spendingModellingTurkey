function iniProject()
    restoredefaultpath;
    close all;
    clc;

    utils.call.paths;
    addpath(genpath(project_path));
    addpath(iris_path);
    iris.startup();

    addpath(dynare_path);
    dynare_config();
end

project_path = string(fileparts(fileparts(fileparts(mfilename('fullpath')))));

iris_path = string(getenv('IRIS_PATH'));
if strlength(iris_path) == 0
    iris_path = "/Users/kk/Documents/0000-00_work/2021-03_iris/iris_live";
end

dynare_path = string(getenv('DYNARE_PATH'));
if strlength(dynare_path) == 0
    dynare_path = "/Applications/Dynare/5.5-arm64/matlab";
end

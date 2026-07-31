function [ys,params,check] = modelTemplate_steadystate(ys,exo,M_,options_)
% computes the steady state, using Steady_states_solution.m for the model
% equations
% Inputs:
%   - ys        [vector] vector of initial values for the steady state of
%                   the endogenous variables
%   - exo       [vector] vector of values for the exogenous variables
%   - M_        [structure] Dynare model structure
%   - options   [structure] Dynare options structure
%
% Output:
%   - ys        [vector] vector of steady state values for the the endogenous variables
%   - params    [vector] vector of parameter values
%   - check     [scalar] set to 0 if steady state computation worked and to
%                    1 of not (allows to impose restrictions on parameters)

% read out parameters to access them with their name
NumberOfParameters = M_.param_nbr;
for ii = 1:NumberOfParameters
    paramname = M_.param_names{ii};
    eval([ paramname ' = M_.params(' int2str(ii) ');']);
end
% initialize indicator
check = 0;

Steady_states_solution;

%% END OF THE MODEL SPECIFIC BLOCK.


%% DO NOT CHANGE THIS PART.
%%
%% Here we define the steady state values of the endogenous variables of
%% the model.
%%
%% end own model equations

params=NaN(NumberOfParameters,1);
for iter = 1:length(M_.params) %update parameters set in the file
    eval([ 'params(' num2str(iter) ') = ' M_.param_names{iter} ';' ])
end

NumberOfEndogenousVariables = M_.orig_endo_nbr; %auxiliary variables are set automatically
for ii = 1:NumberOfEndogenousVariables
    varname = M_.endo_names{ii};
    eval(['ys(' int2str(ii) ') = ' varname ';']);
end                                                        % End of the loop.

function lambda = channel_length_modulation(data, method)
%CHANNEL_LENGTH_MODULATION Extract channel-length modulation parameter.
%
% Description:
%   Estimate the channel-length modulation parameter (λ)
%   from output characteristics.
%
% Inputs:
%   data
%   method
%       "linear"
%       "regression"
%
% Outputs:
%   lambda
%
% Author:
%   Jianhao Wu
%
% Repository:
%   MOSFET Parameter Extraction Toolkit
%
% Version:
%   v1.0

%% Default Method

if nargin < 2
    method = "linear";
end

%% Read Data

VDS = data.VDS;
IDS = data.IDS;

%% Select Method

switch lower(method)

    case "linear"

        % To be implemented
        lambda = [];

    case "regression"

        % To be implemented
        lambda = [];

    otherwise

        error("Unknown channel-length modulation extraction method.");

end

end

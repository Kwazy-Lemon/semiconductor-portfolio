function lambda = channel_length_modulation(data)
%CHANNEL_LENGTH_MODULATION Extract channel-length modulation parameter.
%
% Description:
%   Estimate the channel-length modulation parameter (lambda)
%   from the output characteristics.
%
% Inputs:
%   data.VDS
%   data.IDS
%
% Outputs:
%   lambda
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

%% Read Data

VDS = data.VDS;
IDS = data.IDS;

%% Linear Regression

p = polyfit(VDS, IDS, 1);

slope = p(1);

intercept = p(2);

%% Channel-Length Modulation

lambda = slope / intercept;

%% Display

fprintf("\n");
fprintf("=====================================\n");
fprintf(" Channel-Length Modulation\n");
fprintf("=====================================\n");
fprintf("Lambda = %.4e 1/V\n", lambda);
fprintf("=====================================\n");

end

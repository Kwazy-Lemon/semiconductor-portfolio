function [Vth, fit] = linear_extraction(data)
%LINEAR_EXTRACTION Threshold voltage extraction using Linear Extrapolation.
%
% Inputs:
%   data.VGS
%   data.IDS
%
% Outputs:
%   Vth  - Threshold Voltage
%   fit  - Structure containing fitting information
%
% Author:
%   Jianhao Wu

VGS = data.VGS;
IDS = data.IDS;

gm = gradient(IDS, VGS);

[~, idx] = max(gm);

start_idx = max(1, idx-5);
end_idx   = min(length(VGS), idx+5);

range = start_idx:end_idx;

p = polyfit(VGS(range), IDS(range), 1);

slope = p(1);
intercept = p(2);

Vth = -intercept / slope;

fit = struct();

fit.slope = slope;
fit.intercept = intercept;

fit.range = range;

fit.VGS = VGS(range);
fit.IDS = IDS(range);

fit.gm = gm;
fit.max_index = idx;

fit.start_index = start_idx;
fit.end_index = end_idx;

fit.method = "Linear Extrapolation";

end

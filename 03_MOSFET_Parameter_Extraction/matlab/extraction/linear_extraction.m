function Vth = linear_extraction(data)
%LINEAR_EXTRACTION Threshold voltage extraction using linear extrapolation.
%
% Inputs:
%   data.VGS
%   data.IDS
%
% Outputs:
%   Vth

VGS = data.VGS;
IDS = data.IDS;

% Calculate transconductance
gm = gradient(IDS, VGS);

% Find maximum gm
[~, idx] = max(gm);

% Linear fitting around maximum gm
fit_range = max(1, idx-2):min(length(VGS), idx+2);

p = polyfit(VGS(fit_range), IDS(fit_range), 1);

% Linear extrapolation
Vth = -p(2)/p(1);

end

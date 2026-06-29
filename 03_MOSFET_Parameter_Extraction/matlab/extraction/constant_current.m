function Vth = constant_current(data,Iref)
%CONSTANT_CURRENT Threshold voltage extraction using constant current method.
%
% Inputs:
%   data.VGS
%   data.IDS
%   Iref (optional)
%
% Outputs:
%   Vth

if nargin < 2
    Iref = 1e-6;
end

VGS = data.VGS;
IDS = data.IDS;

[~, idx] = min(abs(IDS - Iref));

Vth = VGS(idx);

end

function mu = mobility(data)
%MOBILITY Extract carrier mobility.
%
% Description:
%   Estimate carrier mobility using the linear-region method.
%
% Inputs:
%   data.VGS
%   data.IDS
%   data.VDS
%   data.W
%   data.L
%   data.Cox
%
% Outputs:
%   mu
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

VGS = data.VGS;
IDS = data.IDS;

VDS = data.VDS;

W = data.W;
L = data.L;

Cox = data.Cox;

p = polyfit(VGS, IDS, 1);

slope = p(1);

mu = slope * L / (Cox * W * VDS);

fprintf("\n");
fprintf("=====================================\n");
fprintf(" Mobility Extraction\n");
fprintf("=====================================\n");
fprintf("Mobility = %.4e m^2/Vs\n", mu);
fprintf("=====================================\n");


end



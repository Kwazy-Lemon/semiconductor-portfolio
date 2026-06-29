function Vth = linear_extraction(data)
%LINEAR_EXTRACTION Threshold voltage extraction using linear extrapolation.
%
% Description:
%   Estimate MOSFET threshold voltage using the maximum transconductance
%   linear extrapolation method.
%
% Inputs:
%   data.VGS
%   data.IDS
%
% Outputs:
%   Vth - Threshold Voltage (V)
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

%% Read Data

VGS = data.VGS;
IDS = data.IDS;

%% Smooth Current (reduce numerical noise)

IDS = smoothdata(IDS,"sgolay",7);

%% Calculate Transconductance

gm = gradient(IDS,VGS);

%% Find Maximum gm

[~,idx] = max(gm);

%% Select Linear Region

N = 5;

startIndex = max(1,idx-N);
endIndex   = min(length(VGS),idx+N);

Vfit = VGS(startIndex:endIndex);
Ifit = IDS(startIndex:endIndex);

%% Linear Regression

p = polyfit(Vfit,Ifit,1);

%% Threshold Voltage

Vth = -p(2)/p(1);

%% Display Result

fprintf("\n");
fprintf("=====================================\n");
fprintf(" Threshold Voltage Extraction\n");
fprintf("=====================================\n");
fprintf("Method : Linear Extrapolation\n");
fprintf("Vth    : %.4f V\n",Vth);
fprintf("=====================================\n");

end

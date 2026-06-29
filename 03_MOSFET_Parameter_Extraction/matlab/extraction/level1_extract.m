function parameters = level1_extract(data_transfer,data_output)
%LEVEL1_EXTRACT Complete Level-1 MOSFET Parameter Extraction.
%
% Description:
%   Extract the major Level-1 MOSFET parameters.
%
% Inputs:
%   data - MOSFET dataset
%
% Outputs:
%   parameters - Structure containing extracted parameters
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

fprintf("\n");
fprintf("=========================================\n");
fprintf(" Level-1 MOSFET Parameter Extraction\n");
fprintf("=========================================\n");

Vth = threshold_voltage(data_transfer,"linear");

mu = mobility(data_transfer);

lambda = channel_length_modulation(data_output);

ro = output_resistance(data_output);

parameters = struct();

parameters.Vth = Vth;
parameters.mu = mu;
parameters.lambda = lambda;
parameters.ro = ro;

fprintf("\n");
fprintf("=========================================\n");
fprintf(" Extraction Summary\n");
fprintf("=========================================\n");

fprintf("Threshold Voltage      : %.4f V\n",Vth);
fprintf("Carrier Mobility       : %.4e m^2/Vs\n",mu);
fprintf("Channel Modulation λ   : %.4e 1/V\n",lambda);
fprintf("Output Resistance      : %.4e Ohm\n",ro);

fprintf("=========================================\n");

end

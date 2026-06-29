function parameters = level1_extract(data)
%LEVEL1_EXTRACT Main entry of the MOSFET Parameter Extraction Toolkit.
%
% Description:
%   Extract Level-1 MOSFET compact model parameters from LTspice
%   simulation data.
%
% Inputs:
%   data - Imported I-V dataset
%
% Outputs:
%   parameters - Structure containing extracted parameters.
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

%% Step 1 - Threshold Voltage
Vth = threshold_voltage(data);

%% Step 2 - Carrier Mobility
mu = mobility(data);

%% Step 3 - Channel-Length Modulation
lambda = channel_length_modulation(data);

%% Step 4 - Output Resistance
ro = output_resistance(data);

%% Store Results
parameters.Vth = Vth;
parameters.mu = mu;
parameters.lambda = lambda;
parameters.ro = ro;

end

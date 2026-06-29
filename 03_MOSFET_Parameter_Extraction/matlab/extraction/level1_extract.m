function parameters = level1_extract(data)
%LEVEL1_EXTRACT Main entry of the MOSFET Parameter Extraction Toolkit.
%
% Description:
%   Perform automatic Level-1 MOSFET compact model parameter extraction
%   from LTspice simulation or experimental I-V data.
%
% Inputs:
%   data - Structure containing MOSFET I-V data
%
%          Required fields:
%          data.VGS
%          data.VDS
%          data.IDS
%
% Outputs:
%   parameters - Structure containing extracted parameters
%
%                parameters.Vth
%                parameters.mu
%                parameters.lambda
%                parameters.ro
%                parameters.method
%                parameters.date
%
% Author:
%   Jianhao Wu
%
% Repository:
%   MOSFET Parameter Extraction Toolkit
%
% Version:
%   v1.0
%
% Last Updated:
%   June 2026

%% --------------------------------------------------------
%  Step 1 : Threshold Voltage Extraction
%% --------------------------------------------------------

Vth = threshold_voltage(data,"linear");

%% --------------------------------------------------------
%  Step 2 : Carrier Mobility Extraction
%% --------------------------------------------------------

mu = mobility(data,"analytical");

%% --------------------------------------------------------
%  Step 3 : Channel-Length Modulation Extraction
%% --------------------------------------------------------

lambda = channel_length_modulation(data,"linear");

%% --------------------------------------------------------
%  Step 4 : Output Resistance Estimation
%% --------------------------------------------------------

ro = output_resistance(data,"linear");

%% --------------------------------------------------------
%  Generate Parameter Structure
%% --------------------------------------------------------

parameters = struct();

parameters.Vth = Vth;
parameters.mu = mu;
parameters.lambda = lambda;
parameters.ro = ro;

%% Metadata

parameters.method = "Level-1 Analytical Extraction";

parameters.date = datetime;

parameters.version = "v1.0";

end

function plot_output_curves(data)
%PLOT_OUTPUT_CURVES Plot MOSFET output characteristics.
%
% Description:
%   Plot IDS-VDS curves for multiple gate voltages.
%
% Inputs:
%   data.VDS
%   data.IDS
%   data.VGS
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

figure;

hold on;
grid on;
box on;

plot(data.VDS, data.IDS,'LineWidth',2);

xlabel('V_{DS} (V)');
ylabel('I_{DS} (A)');
title('MOSFET Output Characteristics');

set(gca,'FontSize',12);

end

function plot_linear_fit(data,Vth)

% Plot transfer curve with extracted threshold voltage

VGS = data.VGS;
IDS = data.IDS;

figure;

plot(VGS,IDS,...
    'b',...
    'LineWidth',2);

hold on;

xline(Vth,'--r','LineWidth',2);

plot(Vth,0,...
    'ro',...
    'MarkerFaceColor','r',...
    'MarkerSize',8);

grid on;
box on;

xlabel('V_{GS} (V)');
ylabel('I_D (A)');
title('Linear Extrapolation Threshold Voltage');

legend( ...
    'Transfer Curve',...
    'Extracted V_{th}',...
    'Location','northwest');

set(gca,'FontSize',12);

end

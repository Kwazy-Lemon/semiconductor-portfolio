function plot_transfer_curve(data)

%PLOT_TRANSFER_CURVE Plot Id-VGS transfer characteristic.

VGS = data.VGS;
IDS = data.IDS;

figure;

plot(VGS,IDS,'b','LineWidth',2);

grid on;
box on;

xlabel('V_{GS} (V)');
ylabel('I_D (A)');
title('MOSFET Transfer Characteristics');

set(gca,'FontSize',12);

end

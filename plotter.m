% a good way to start a new script
%clear all
%close all
%clc

% define your data
x=table2array(TelemetryBasedRangingSimulations3(:,1))
y=table2array(TelemetryBasedRangingSimulations3(:,[2:10]))

y=y/208
%hold on 
% plot your data 
figure (1)

plot(x, max(eps, y(:,3)),'-o',x, max(eps, y(:,4)),'-+',x, max(eps, y(:,5)),'-*',x, max(eps, y(:,6)),'-x',x, max(eps, y(:,7)),'-square')

legend('K=1','K=10','K=20','K=50','k=100')
%plot (x, y1, 'r');
txt = {'K=No of Codewords Integrated'};
%plot (x, y3,'-go', 'MarkerFaceColor', 'green')
xlabel('SNR [Hz]')
ylabel('Delay Error [Symbols]')
set(gca, 'YScale', 'log')
title('Telemetry Ranging Simulation Performance(With Demod Remod)')
xlim([-50 50])
grid on

%hold off


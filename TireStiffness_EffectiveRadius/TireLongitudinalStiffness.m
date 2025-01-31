function [Cx, Re] = TireLongitudinalStiffness(a,m,V,w)
a(1:4)= []; % Outliers
V(1:4)= [];
w(1:4)= [];

p = w./V; % Calculate the speed ratio with linear velocity / angular velocity
P = [ones(length(p),1) p']; % Append column of 1s to find the intercept in the next step
c_m = P\a'; % Use built in least squares regression to find the slope and intercept
c = 100*c_m(1); % First column is intercept, 2nd is slope
M = 100*c_m(2);

Cx = -c*m;
Re = m*M/Cx;
end
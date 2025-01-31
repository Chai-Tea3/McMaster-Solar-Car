function [x] = fun_nonLinForce(m,Ru,Rd,Cx,t_u,dt_u,ddt_u,t_d,dt_d,ddt_d)

% Deltas are supposed to be the error in each measurement...
delta_dt_u = dt_u - dt_d;
delta_ddt_u = ddt_u - ddt_d;
delta_dt_d = 0;

x = m*Ru^2*(t_u + delta_ddt_u)*(t_u + delta_dt_u) + Cx*(Ru*(t_u + delta_dt_u) - Rd*(t_d + delta_dt_d));

end
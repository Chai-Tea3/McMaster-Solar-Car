t = 40; % Total time [s]
samplingRate = 10; % [Hz]
N = t*samplingRate;

t_u = zeros(1, N+1); % Theta undriven/driven wheels with derivatives
dt_u = zeros(1, N+1);
ddt_u = zeros(1, N+1);
t_d = zeros(1, N+1);
dt_d = zeros(1, N+1);
ddt_d = zeros(1, N+1);
Cx_final = zeros(1, N+1);
Re_final = zeros(1, N+1);

t_u(1) = 0;
dt_u(1) = 0;
ddt_u(1) = 0;
t_d(1) = 0;
dt_d(1) = 0;
ddt_d(1) = 0;

time = zeros(1, N+1);
V_clean = zeros(1, N+1);
V = zeros(1, N+1);
wd_clean = zeros(1, N+1);
wd = zeros(1, N+1);
accel = zeros(1, N+1);

time(1) = 0;
V_clean(1) = 8; % Matching the inital conditions to the article
V(1) = 8;
wd_clean(1) = 26.7;
wd(1) = 26.7;
accel(1) = 3;

m = 200; % Mass [kg]
R = 0.3; % Tire Radius [m]

vehicle_accel = 3; % [m/s^2]
vehicle_decel = -1; % [m/s^2]


% Generate clean velocity and convert to noisy angular velocity
for n = 1:N
    time(n+1) = time(n) + (1/samplingRate);

    u = rand(1); % Generate probability from 0,1
    x = norminv(u,0,0.04); % Inverse Transform for normal distribution w/ SD = 0.04rad

    V_clean(n+1) = V_clean(n) + (1/samplingRate)*(accel(n));
    wd_clean(n+1) = V_clean(n)/R;
    wd(n+1) = wd_clean(n) + x; % Add noise to the angular velocity

    % Accelerate and decelerate with period of 10s
    if(mod(time(n),10) > 0 && mod(time(n),10) < 2.5)
        accel(n+1) = vehicle_accel;
    elseif(mod(time(n),10) > 2.5 && mod(time(n),10) < 10)
        accel(n+1) = vehicle_decel;
    end
end


% Use noisy angular velocity to find actual velocity and acceleration
for n = 1:N
    V(n+1) = wd(n)*R;
    accel(n+1) = samplingRate*(V(n+1) - V(n));
end

% Initial guess using linear regression
% Re guess is very accurate, Cx off by magintude of 10s
[Cx_guess, Re_guess] = TireLongitudinalStiffness(accel,m,V,wd); 


for n = 1:N
    % Finds theta for both the driven/undriven wheen and its time derivatives
    % Using angular velocity simulated earlier, assume driven is clean,
    % undriven has noise?
    t_u(n+1) = t_u(n) + wd(n);
    dt_u(n+1) = wd(n);
    ddt_u(n+1) = samplingRate*(dt_u(n+1) - dt_u(n));
    t_d(n+1) = t_d(n) + wd_clean(n);
    dt_d(n+1) = wd_clean(n);
    ddt_d(n+1) = samplingRate*(dt_d(n+1) - dt_d(n));

    fun1 = @(x)fun_nonLinForce(m,R,Re_guess,x,t_u(n),dt_u(n),ddt_u(n),t_d(n),dt_d(n),ddt_d(n));
    Cx_final(n+1) = lsqnonlin(fun1,Cx_guess); % Solve for Cx using the initial conditions
end

Cx_final(1:3) = [];
Cx = mean(Cx_final);

for n = 1:N
    % Solve for Re using new Cx value
    % Can probably use the value obtained from 1st method, only Cx requires
    % more complicated algorithm.

    fun2 = @(x)fun_nonLinForce(m,R,x,Cx,t_u(n),dt_u(n),ddt_u(n),t_d(n),dt_d(n),ddt_d(n));
    Re_final(n+1) = lsqnonlin(fun2, Re_guess); 
end

Re_final(1:3) = [];
Re = mean(Re_final);


subplot(3, 1, 1)
plot(time, V)
title("Simulated Velocity")                     % title       
xlabel("Time [s]"); ylabel("Velocity [m/s]")    % axis labels
xlim([0, 40]);                                  % axis limits

subplot(3, 1, 2)
plot(time, wd)
title("Simulated Angular Velocity")             % title
xlabel("Time [s]"); ylabel("Ang Vel [rad/s]")   % axis labels
xlim([0,40]);                                   % axis limits

subplot(3, 1, 3)
plot(time, accel)
title("Simulated Acceleration")                 % title
xlabel("Time [s]"); ylabel("Accel [m/s^2]")     % axis labels
xlim([0,40]);                                   % axis limits

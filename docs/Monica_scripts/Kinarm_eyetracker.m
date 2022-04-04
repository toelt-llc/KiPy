%% KINARM DATA ANALYSIS - eye tracker
%Loading data
clear
alldata= exam_load

%Extract data of Arm Positioning Match RIGHT hand 
APM_R = alldata(2).c3d; 
tp= APM_R(1).TRIAL.TP %extract trial protocol for first event 
target=APM_R(1).TP_TABLE.Target(tp)

%Plot APM_RIGHT HAND position over trials 
figure
for t  = 1:24; 
    plot(APM_R(t).Right_HandX, APM_R(t).Right_HandY)
hold on; 
print('CP 11 VGR DH','-dpng')
end
ylabel('Y (m)');
xlabel('X (m)');
title ('CP 11 APM DH- Right Hand Paths (all trials)');

%Write table with target position over trials
APM_R = alldata(2).c3d;
 for t= 1:24
     tp = APM_R(t).TRIAL.TP;
     targetTP = APM_R(t).TP_TABLE.Target(tp);
     target(t,1) = APM_R(t).TARGET_TABLE.X(targetTP);
      target(t,2) = APM_R(t).TARGET_TABLE.Y(targetTP);
 end 
 
writematrix(target,'parameters_APM_r')


%Extract data of Arm Positioning Match LEFT hand 
APM_L = alldata(4).c3d; 
tp= APM_L(1).TRIAL.TP %extract trial protocol for first event 
target=APM_L(1).TP_TABLE.Target(tp)

%Plot APM_RIGHT HAND position over trials 
for t  = 1:25; plot(APM_L(t).Left_HandX, APM_L(t).Left_HandY)
hold on; end

%Write table with target position over trials
APM_L = alldata(4).c3d;
 for t= 1:25
     tp = APM_L(t).TRIAL.TP;
     targetTP = APM_L(t).TP_TABLE.Target(tp);
     target(t,1) = APM_L(t).TARGET_TABLE.X(targetTP);
      target(t,2) = APM_L(t).TARGET_TABLE.Y(targetTP);
 end 
 
writematrix(target,'parameters_APM_l')


%Extract data of Ball on bar
BOB = alldata(6).c3d; 
tp= BOB(1).TRIAL.TP %extract trial protocol for first event 
target=BOB(1).TP_TABLE.Target(tp)

%Plot APM_RIGHT HAND position over trials 
for t  = 1:3; plot(BOB(t).Left_HandX, BOB(t).Left_HandY)
hold on
plot(BOB(t).Right_HandX, BOB(t).Right_HandY)
end;

%Write table with target position over trials
BOB = alldata(6).c3d;
 for t= 1:3
     tp = BOB(t).TRIAL.TP;
     targetTP = BOB(t).TP_TABLE.Target(tp);
     target(t,1) = BOB(t).TARGET_TABLE.X(targetTP);
      target(t,2) = BOB(t).TARGET_TABLE.Y(targetTP);
 end 
 
writematrix(target,'parameters_BOB')

%Extract data of Object hit 
OH = alldata(8).c3d; 


%Plot APM_RIGHT HAND position over trials 
for t  = 1:1; plot(OH(t).Left_HandX, OH(t).Left_HandY)
hold on
plot(OH(t).Right_HandX, OH(t).Right_HandY)
end;

%Write table with target position over trials
OH = alldata(8).c3d;
 for t= 1:1
     tp = OH(t).TRIAL.TP;
     target(t,1) = OH(t).TARGET_TABLE.X(tp);
      target(t,2) = OH(t).TARGET_TABLE.Y(tp);
 end 
 
writematrix(target,'parameters_OH')

%Extract data of Visually guided RIGHT hand 
VG_R = alldata(19).c3d; 
tp= VG_R(1).TRIAL.TP %extract trial protocol for first event 

%Plot VG_RIGHT HAND position over trials 
for t  = 1:24; plot(VG_R(t).Right_HandX, VG_R(t).Right_HandY)
hold on; end

%Extract data of Visually guided LEFT hand 
VG_L = alldata(18).c3d; 
tp= VG_L(1).TRIAL.TP %extract trial protocol for first event 

%Plot VG_LIGHT HAND position over trials 
for t  = 1:24; plot(VG_L(t).Left_HandX, VG_L(t).Left_HandY)
hold on; end

%% EYE-TRACKER EVENTS - CALCULATE DURATION 
EVENTS_armpos_R = {alldata(2).c3d.EVENTS}.'

%if string returns value 
if strncmp('Gaze saccade start', alldata(2).c3d(1).EVENTS.LABELS(3), 18); 
    x= alldata(2).c3d(1).EVENTS.TIMES(3); 
end

%SACCADES
%Find all the 'gaze saccade start' values
for i =1:35
if strncmp('Gaze saccade start', alldata(2).c3d(1).EVENTS.LABELS(i), 18); 
    a(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end 
   
%Find all the 'Gaze saccade end' values
for i =1:35
if strncmp('Gaze saccade end', alldata(2).c3d(1).EVENTS.LABELS(i), 16); 
    b(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end

%Duration of saccades
sac_starts=nonzeros(a);
sac_ends= nonzeros(b);
sac_duration = (sac_ends-sac_starts); %if first saccades t = 0 error (remember to add 0)

%FIXATIONS 
%Find all the 'fixation start' values
for i =1:37
if strncmp('Gaze fixation start', alldata(2).c3d(1).EVENTS.LABELS(i), 19); 
    c(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end 
   
%Find all the 'fixation end' values
for i =1:37
if strncmp('Gaze fixation end', alldata(2).c3d(1).EVENTS.LABELS(i), 17); 
    d(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end

%Duration of saccades
fix_starts=nonzeros(c);
fix_ends= nonzeros(d);
fix_duration = (fix_ends-fix_starts);
   
%BLINKS 
%Find all the 'blink start' values
for i =1:37
if strncmp('Gaze blink start', alldata(2).c3d(1).EVENTS.LABELS(i), 16); 
    e(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end 
   
%Find all the 'blink end' values
for i =1:37
if strncmp('Gaze blink end', alldata(2).c3d(1).EVENTS.LABELS(i), 14); 
    f(i)= alldata(2).c3d(1).EVENTS.TIMES(i); 
end
end

%Duration of saccades
blink_starts=nonzeros(e);
blink_ends= nonzeros(f);
blink_duration = (blink_ends-blink_starts);
%% EYE-TRACKER EVENTS
%Extract eye-tracker events for each task into a cell array 
EVENTS_armpos_R = {alldata(2).c3d.EVENTS}.' %24x1 cell array --> 24 trials --> first sheet 
EVENTS_armpos_L = {alldata(4).c3d.EVENTS}.' %25x1 cell array --> 25 trials
EVENTS_ballonbar = {alldata(6).c3d.EVENTS}.' %3x1 cell array 
EVENTS_objhit = {alldata(8).c3d.EVENTS}.'%1x1 cell array
EVENTS_visguided_R = {alldata(19).c3d.EVENTS}.' %24x1 cell array --> 24 trials
EVENTS_visguided_L = {alldata(18).c3d.EVENTS}.' %24x1 cell array --> 24 trials
%In each cell array I want to extarct LABELS and TIMES into a single sheet
%in excel --> 
%Thus I will have in the first sheet 

%row 1 --> EVENTS_armpos_R.LABELS(1)
%row 2 --> EVENTS_armpos_R.TIMES(1)
%row 3 --> EVENTS_armpos_R.LABELS(2)
%row 4 --> EVENTS_armpos_R.TIMES(2)
% ..... till %row 47 --> EVENTS_armpos_R.LABELS(24)
%row 48 --> EVENTS_armpos_R.TIMES(24)

%see file excel attached 

%Ho provato a fare questo ma ovviamentr non va perchè hanno diemensioni
%diverse 

% X=[{'EVENTS_armpos_R ','EVENTS_armpos_L','EVENTS_ballonbar ','EVENTS_objhit','EVENTS_visguided_R','EVENTS_visguided_L'};EVENTS_armpos_R,
% EVENTS_armpos_L ,
% EVENTS_ballonbar,
% EVENTS_objhit ,
% EVENTS_visguided_R ,
% EVENTS_visguided_L]
% xlswrite('X.xls',X)
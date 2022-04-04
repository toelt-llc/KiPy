function [ smoothPursuitsVector ] = computegazeEventClassification(gazeTargetMatrix,minPursuitDuration)
%This function computes gaze events based on Equations 1-12 in the manuscript.
%Please cite the paper as:
%Singh, T., Perry, C., & Herter, T. (2015). A geometric method for computing ocular 
%kinematics and classifying gaze events using monocular remote eye tracking in 
%a robotic environment. Journal of Neuroengineering and Rehabilitation.

%Created by Tarkeshwar Singh, October 2015

%% This section initializes sampling frequency (Fs), 
% the parameters for the Savitzky Golay Filter (Equation 4),
% noise_threshold (Eq. 11, 12), Rotation Matrix (Eq. 2), H (Equation 2),
% visual_angle (Eq. 9), and calibration_error (Eq. 9). 
     Fs=1e3;
     savitzky_golay_filter_parameter.f=41;
     savitzky_golay_filter_parameter.k=8;
     noise_threshold_eta=0.2;
     Rotation_Matrix=eye(3); %We assume a simple rotation matrix for Equation 1. 
     H=330;   %Specify this value in mm. 
     visual_angle=3.0;
     calibration_error=0.5;  %This is not a constant and will vary from subject to subject. 
     delta=visual_angle+calibration_error;
     %% This section takes the input matrix, gazeTargetMatrix. 
     %Column 1: Gaze Timestamps.
     %Column 2: Gaze X Coordinates in the XYZ frame. 
     %Column 3: Gaze Y Coordinates in the XYZ frame.
     %Column 4: Target X Coordinates in the XYZ frame.
     %Column 5: Target Y Coordinates in the XYZ frame. 
     %Column 6: Target X Velocity in the XYZ frame.
     %Column 7: Target Y Velocity in the XYZ frame.
     
     Gaze_TimeStamp=gazeTargetMatrix(:,1);
     Gaze_X=gazeTargetMatrix(:,2);
     Gaze_Y=gazeTargetMatrix(:,3);
    
     Target_X=gazeTargetMatrix(:,4);
     Target_Y=gazeTargetMatrix(:,5);
     Target_Velocity_Euclidean=(bsxfun(@hypot, gazeTargetMatrix(:,6), gazeTargetMatrix(:,7)));
     Target_Velocity_Angular=computeTargetSphericalVelocity(Target_X,Target_Y,Fs,savitzky_golay_filter_parameter);
     %% This section computes the gaze angular velocity (Eq. 6a)
    Gaze_prime=repmat([0;0;H],1,length(Gaze_X))+Rotation_Matrix*[Gaze_X Gaze_Y zeros(length(Gaze_X),1)]';
    Gaze_prime=Gaze_prime';
    Gaze_X_prime=Gaze_prime(:,1);
    Gaze_Y_prime=Gaze_prime(:,2);
    Gaze_Z_prime=Gaze_prime(:,3);
    
    
    Gaze_X_prime_dot_nofilt=derivative(Gaze_X_prime)./derivative(Gaze_TimeStamp);
    Gaze_X_prime_dot=sgolayfilt(Gaze_X_prime_dot_nofilt,savitzky_golay_filter_parameter.k,savitzky_golay_filter_parameter.f);
    Gaze_Y_prime_dot_nofilt=derivative(Gaze_Y_prime)./derivative(Gaze_TimeStamp);
    Gaze_Y_prime_dot=sgolayfilt(Gaze_Y_prime_dot_nofilt,savitzky_golay_filter_parameter.k,savitzky_golay_filter_parameter.f);
    Gaze_Z_prime_dot=0;
    Gaze_Abs_dot_prime=sqrt(Gaze_X_prime_dot.^2+Gaze_Y_prime_dot.^2+Gaze_Z_prime_dot.^2);
            
    [theta,phi,rho] = cart2sph(Gaze_X_prime, Gaze_Y_prime,Gaze_Z_prime);
    
    rho_dot=((Gaze_X_prime.*Gaze_X_prime_dot)+(Gaze_Y_prime.*Gaze_Y_prime_dot)+(Gaze_Z_prime.*Gaze_Z_prime_dot))./(rho);
    denominator_theta=(Gaze_X_prime.^2+Gaze_Y_prime.^2);
    numerator_theta=(Gaze_Y_prime.*Gaze_X_prime_dot)-(Gaze_X_prime.*Gaze_Y_prime_dot);
    theta_dot=(numerator_theta./denominator_theta).*cos(phi);
    
    numerator_phi=Gaze_Z_prime.*((Gaze_X_prime.*Gaze_X_prime_dot)+(Gaze_Y_prime.*Gaze_Y_prime_dot));   %The second term in the numerator is zero because Gaze_Z_prime_dot=0;
    denominator_phi=(rho.^2).*sqrt(denominator_theta);
    phi_dot= numerator_phi./denominator_phi;
    
    gazeVelocityVector=(bsxfun(@hypot, theta_dot, phi_dot))*(180/pi); %Convert to Degrees. 
    gazeAccVector_noFilt=derivative(gazeVelocityVector)*Fs;
    gazeAccelerationVector=sgolayfilt(gazeAccVector_noFilt,savitzky_golay_filter_parameter.k,savitzky_golay_filter_parameter.f);
    
    %% This section computes the Foveal Visual Radius (Eq. 9)
    FVR=rho*tand(delta*0.5).*csc(asin(H./rho)); 
        
    %% This section computes the saccade velocity threshold (Eq. 10a)
    gazeVelocityThreshold=computegazeVelocityThreshold(gazeVelocityVector);
    %This function is appended below in the file. 
    
    %% This condition checks for the condition in Eq. 12 for smooth pursuits.  
       
    Tr=ones(length(Gaze_X_prime),1)*10; %Convert Tr to mm by multiplying it with 10. 
    Dist_X=Gaze_X_prime-Target_X;
    Dist_Y=Gaze_Y_prime-Target_Y;
    Abs_Dist_Gaze_Hand=(bsxfun(@hypot, Dist_X, Dist_Y));
    
    gazeEventVector=computeGazeEventVector(gazeVelocityVector,gazeVelocityThreshold,Fs,minPursuitDuration,gazeAccelerationVector);
    %This function returns a vector classifying all saccades as 1s and
    %everything else as zero. Fixations and smooth pursuits should be
    %searched in the vector elements that are '0'. This function implements
    %the checks in Equations 12 c-d. 
    
    gazeEventVector((Abs_Dist_Gaze_Hand<=(1+noise_threshold_eta)*(FVR+Tr)) & gazeEventVector==0)=2; %Assign gaze events to 2 (smooth pursuits) if Eq. 12a is satisifed. 
    gazeEventVector(abs(Target_Velocity_Angular-gazeVelocityVector)>(noise_threshold_eta*gazeVelocityVector))=0; % If 12b is not satisfied, then turn events back to unclassified. 
     
    
    [c,valnew] = accumconncomps(gazeEventVector);
    Z=  [c,valnew];
    smoothPursuitsVector=length(find(Z(:,1)==2 & Z(:,2)>=minPursuitDuration));

end



%% Function to compute the gazeVelocityThreshold
%One thing to note while using this function is that the input vector
%should comprise of multiple trials (discrete tasks) or as many time points
%as possible if the task is continuous. The more the data points, the
%better the estimate of the saccade velocity threshold.

function varargout= computegazeVelocityThreshold(varargin)

%This function computes and plots the parameters of a bimodal lognormal
%plot. The input data for this function is just a vector. 

% INPUTS:
%Data_Vector      =       gaze velocity vector after blink correction and artifact removal. 
%This value should be in degree/sec. 
%Max_Iteration_MLE      =   maximum iterations for mle
%Max_Fun_Evals_MLE      =     PDF function evaluation limit
%pStart     =       default value 0.2. Shows the mixing ratio of the two pdfs.
%We start with 0.2 unless otherwise specified. 
%Data_Peak_Threshold    =   This threshold is required to determine a lower
%bound for the findpeaks function. Any velocity peak below the Threshold
%will be ignored. The default value for this is 0.05. 
%Bin Size = Self-explanatory. 
%Gaze_Fs = Sampling Frequency of the Gaze Data

% OUTPUTS:
%   Velocity_Threshold = Gaze Velocity Threshold based on the lognormal plot.
%   ParamEsts     = Estimates of the parameters of the bimodal lognormal distribution.
%   h     = Graphic handle for the bar plot.
%   PDFGRID        = The fitted PDF function.


%The easiest way to use the function is:
%gazeVelocityThreshold=computegazeVelocityThreshold(Data_Vector);

%More details about the implementation can be found here
%(http://www.mathworks.com/help/stats/examples/fitting-custom-univariate-distributions.html)

%Copyright: Tarkeshwar Singh 2015. Dept. of Exercise Science,USC, Columbia,SC.

%% This section sets the initial parameters if they are not entered as inputs. 
Max_Iteration_MLE=600;
Max_Fun_Evals_MLE =800;
pStart=0.1;
muStart_Range = [.15 .85];
Data_Peak_Threshold=0.5;
Bin_Size=.2;
Gaze_Fs=500;  
%% This variable looks for local velocity peaks that are at least 50 ms apart. 
gaze_threshold_ts=50/(1000/(Gaze_Fs)); %Set it to 50 ms 
%% This section takes the input parameters and assigns them to local variables. 

if nargin <1
    error('myApp:argChk', 'Wrong number of input arguments');
 
elseif nargin ==1
Data_Vector=varargin{1};

elseif nargin==2
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};

elseif nargin ==3
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};
Max_Fun_Evals_MLE =varargin{3};

elseif nargin==4
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};
Max_Fun_Evals_MLE =varargin{3};
pStart=varargin{4};

elseif nargin==5
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};
Max_Fun_Evals_MLE =varargin{3};
pStart=varargin{4};
muStart_Range = varargin{5};

elseif nargin==6
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};
Max_Fun_Evals_MLE =varargin{3};
pStart=varargin{4};
muStart_Range = varargin{5};
Data_Peak_Threshold=varargin{6};

elseif nargin==7
Data_Vector=varargin{1};
Max_Iteration_MLE=varargin{2};
Max_Fun_Evals_MLE =varargin{3};
pStart=varargin{4};
muStart_Range = varargin{5};
Data_Peak_Threshold=varargin{6};
Bin_Size=varargin{7};

elseif nargin>7
   error('myApp:argChk', 'Wrong number of input arguments');
   
end

%% 

%Body of Function
%% 

[pks,locs] = findpeaks(Data_Vector,'minpeakheight',Data_Peak_Threshold,'minpeakdistance',gaze_threshold_ts);
% This function computes local velocity peaks under two constraints: a)
% minpeakheight (velocity should be at least 0.5 deg/s, default or user
% specified value); and b) minpeakdistance (peaks should be separated a certain distance).
% The local peaks are also log transformed here. 
lengthDataVector=length(Data_Vector);
Sorted_Peak_Vector=sort(pks);
x=log(Sorted_Peak_Vector);  %Log transform of the local velocity peaks. 



%% We now define the model and provide the intial guess for the parameters. 
%The PDF for a mixture of two normals is just a weighted sum of the PDFs of 
%the two normal components, weighted by the mixture probability. 
pdf_normmixture = @(x,p,mu1,mu2,sigma1,sigma2) p*normpdf(x,mu1,sigma1) + (1-p)*normpdf(x,mu2,sigma2);
muStart = quantile(x,muStart_Range);
sigmaStart = sqrt(var(x) - .25*diff(muStart).^2);
start = [pStart muStart sigmaStart sigmaStart];
lb = [0 -Inf -Inf 0 0];
ub = [1 Inf Inf Inf Inf];
%% 
options = statset('MaxIter',Max_Iteration_MLE, 'MaxFunEvals',Max_Fun_Evals_MLE);
paramEsts = mle(x, 'pdf',pdf_normmixture, 'start',start, 'lower',lb, 'upper',ub, 'options',options);
%% This section creates a plot of the bimodal lognormal distribution                   
bins = 0:Bin_Size:max(x);
figure('Color',[1 1 1]);
h=bar(bins,histc(x,bins)/(length(x)*Bin_Size),'histc');
set(h,'FaceColor',[.9 .9 .9],'linewidth',2);
xgrid = linspace(1.1*min(x),1.1*max(x),200);
pdfgrid = pdf_normmixture(xgrid,paramEsts(1),paramEsts(2),paramEsts(3),paramEsts(4),paramEsts(5));
hold on; plot(xgrid,pdfgrid,'LineWidth',5, 'LineStyle','-', 'Color','m'); hold off
xlabel('Ln(Velocity) of Local Peaks', 'fontsize',24,'fontweight','b','color','k'); 
ylabel('Probability Density Function','fontsize',24,'fontweight','b','color','k');
set(gca,'FontSize',24);
set(gca, 'box', 'off');
axis tight

%% This section creates the output variables. 
varargout{4}=pdfgrid;
paramEsts(6)=(paramEsts(3)-paramEsts(2))/(2*(paramEsts(4)+paramEsts(5)));
varargout{2}=paramEsts;
varargout{3}=h;

lower_saccade_vel=paramEsts(3)-(2*paramEsts(5));
upper_fixation_vel=paramEsts(2)+(2*paramEsts(4));
Velocity_Threshold=exp(0.5*((lower_saccade_vel)+(upper_fixation_vel)));

% Note that if the distribution is not bimodal, the threshold would be biased. 

varargout{1}=Velocity_Threshold;
h2=vline(log(Velocity_Threshold),'g');
set(gca,'LineWidth',2);
set(h2,'LineWidth',2);
text(log(Velocity_Threshold)+0.1,0.4,strcat(num2str(round(Velocity_Threshold)),'^{\circ}','/s'),'fontsize',24,'fontname','Helvetica') 

%% This section plots a sub section of the gaze velocity data along with the 
% velocity threshold computed using our method and the 30 deg/sec value
% reported in the literature.

figure('Color',[1 1 1]);
PeakSig=Data_Vector((lengthDataVector/4+1):(lengthDataVector/2));
time_vector=1:1:length(PeakSig);
[pks,locs] = findpeaks(PeakSig,'minpeakheight',Velocity_Threshold,'minpeakdistance',25);
h1=plot(time_vector,PeakSig,'linewidth',3);
hold on
h2=plot(time_vector(locs),pks+0.05,'k^','markerfacecolor',[1 0 0]);
hold off
xlabel('Time (ms)', 'fontsize',28,'fontweight','b','color','k'); 
ylabel('Velocity (^o/s)','fontsize',28,'fontweight','b','color','k');
set(gca,'FontSize',24);
set(gca, 'box', 'off');
set(h2,'markersize',12)
axis tight
h3=hline(Velocity_Threshold,'g');
set(gca,'LineWidth',2);
set(h3,'LineWidth',6);
h4=hline(20,'c');
set(gca,'LineWidth',2);
set(h4,'LineWidth',6);

end

%% Function to compute the gaveEventVector
%This function creates an event vector for saccades. All time points that
%qualify as saccades are marked as '1' and everything else is left
%unassigned as '0'. 

function [varargout] = computeGazeEventVector(gazeVelocityVector,saccadeVelocityThreshold,Fs,minFixationDuration,gazeAccelerationVector)
%This function searches for inflection points on either sides of a saccade
%and also verifies that the acceleration leading up to the velocity peak
%exceeded the acceleration threshold of 6000 deg/sec^2. 

% INPUTS:
%gazeVelocityVector: gaze velocity vector. 
%saccadeVelocityThreshold: Obtained from the function
%computegazeVelocityThreshold.
%Fs : Sampling Frequency.
%minFixationDuration : We have set it at 40 ms. 
%gazeAccelerationVector: gaze acceleration vector

% OUTPUTS:
%  onsetVelocityThreshold: The gaze velocity at which a saccade begins. 
%  offsetVelocityThreshold: The gaze velocity at which a saccade
%  terminates. 
% gazeEventVector: outputs 1 for time points that qualify as saccade and 0
% otherwise.

%The easiest way to use the function is:
%gazeEventVector=computeGazeEventVector(gazeVelocityVector,saccadeVelocityThreshold,Fs,minFixationDuration,gazeAccelerationVector);

%Copyright: Tarkeshwar Singh 2015. Dept. of Exercise Science,USC, Columbia,SC.
%% Saccade Acceleration Threshold
saccadeAccThreshold=6e3;

%% This section plots the gaze anglualr velocity and also the saccade velocity threshold.  
PeakSig=gazeVelocityVector;
x=1:1:length(PeakSig);
[pks,locs] =findpeaks(PeakSig,'MINPEAKHEIGHT',saccadeVelocityThreshold,'MINPEAKDISTANCE',(minFixationDuration*Fs/1e3)); %50 ms because we assume min fixation or sp is ~40 ms (6 points) and min. saccade is 20 (4 points)
figure('Color',[1 1 1]);
plot(x,PeakSig), hold on
plot(x(locs),pks+0.05,'k^','markerfacecolor',[1 0 0],'markersize',10)
h=hline(saccadeVelocityThreshold,'k','Saccade Detection Threshold');
set(h,'Linewidth',2);hold off
xlabel('Time Points (multiples of 5 ms)', 'fontsize',32,'fontweight','b','color','k'); 
ylabel('Gaze Angular Velocity','fontsize',36,'fontweight','b','color','k');
set(gca,'FontSize',28);
set(gca, 'box', 'off','LineWidth',2);
axis tight

%% In this section, we search for inflection points within a 120 time point 
%window. Since we sampled at 1000 Hz, 120 time points is reasonable but at
%lower frequences this value may need to be changed. 
locs_less_120=locs-(120*Fs/1e3);
locs_plus_120=locs+(120*Fs/1e3);
locs_for_onset_offset_search=[locs_less_120 locs locs_plus_120];
locs_for_onset_offset_search(1:3,1)=max(1,locs_for_onset_offset_search(1:3,1));
locs_for_onset_offset_search(end-2:end,3)=min(length(gazeVelocityVector),locs_for_onset_offset_search(end-2:end,3));
gazeEventVector=zeros(length(gazeVelocityVector),1);
gazeEventVector(gazeEventVector==0 & gazeAccelerationVector>=saccadeAccThreshold)=1; %Acceleration Threshold is implemented first. 

for i=1:size(locs_for_onset_offset_search,1)
    
    gaze_velocity_onset_sector=gazeVelocityVector(locs_for_onset_offset_search(i,1):locs_for_onset_offset_search(i,2));
    onset_sector=derivative(gaze_velocity_onset_sector);
    
    if ~isempty(find(onset_sector<0,1,'last'))
    onsetVelocity(i)=gaze_velocity_onset_sector(find(onset_sector<0,1,'last')+1);
    onset_loc=find(onset_sector<0,1,'last')+locs_for_onset_offset_search(i,1); 
    else
    onsetVelocity(i)=8; %approx 8 deg/s is a fair assumption. 
    onset_loc=locs_for_onset_offset_search(i,1);
    end
    
    gaze_velocity_offset_sector=gazeVelocityVector(locs_for_onset_offset_search(i,2):locs_for_onset_offset_search(i,3));
    offset_sector=derivative(gaze_velocity_offset_sector);
    
    if ~isempty(find(offset_sector>0,1,'first')) && (length(gaze_velocity_offset_sector)>=(find(offset_sector>0,1,'first')+1))  
    offsetVelocity(i)=gaze_velocity_offset_sector(find(offset_sector>0,1,'first')+1);
    offset_loc=find(offset_sector>0,1,'first')+locs_for_onset_offset_search(i,2);
    else
    offsetVelocity(i)=9; %9 because of glissades in our data set. 
    offset_loc=locs_for_onset_offset_search(i,3);
    end
    
    gazeEventVector(onset_loc:offset_loc)=1;
end
%% This section computes the onsetVelocityThreshold and offsetVelocityThreshold
%by taking the average of the computed initiation and termination values.
onsetVelocityThreshold=mean(onsetVelocity);
offsetVelocityThreshold=mean(offsetVelocity);
plot(gazeEventVector,'r')
varargout{1}=gazeEventVector;
varargout{2}=onsetVelocityThreshold;
varargout{3}=offsetVelocityThreshold;

end
%% This function computes the angular velocity of the targets. 
function [TargetVelocityVector] = computeTargetSphericalVelocity(Target_X,Target_Y,Fs,savitzky_golay_filter_parameter)
%This function computes T_dot_phi_theta (Eq. 12b).
%Inputs:
%Target_X: Vector of X coordinates of target.
%Target_Y: Vector of Y coordinates of target.
%Fs: Sampling Frequency. 
%savitzky_golay_filter_parameter: Filter parameters. 

%Output:
%TargetVelocityVector: Target Velocity in Spherical Coordinates. 

    Rotation_Matrix=eye(3); %We assume a simple rotation matrix for Equation 1. 
    H=330;   %Specify this value in mm. 

    Target_prime=repmat([0;0;H],1,length(Target_X))+Rotation_Matrix*[Target_X Target_Y zeros(length(Target_X),1)]';
    Target_prime=Target_prime';
    Target_X_prime=Target_prime(:,1);
    Target_Y_prime=Target_prime(:,2);
    Target_Z_prime=Target_prime(:,3);
    
    
    Target_X_prime_dot_nofilt=derivative(Target_X_prime)*Fs;
    Target_X_prime_dot=sgolayfilt(Target_X_prime_dot_nofilt,savitzky_golay_filter_parameter.k,savitzky_golay_filter_parameter.f);
    Target_Y_prime_dot_nofilt=derivative(Target_Y_prime)*Fs;
    Target_Y_prime_dot=sgolayfilt(Target_Y_prime_dot_nofilt,savitzky_golay_filter_parameter.k,savitzky_golay_filter_parameter.f);
    Target_Z_prime_dot=0;
    Target_Abs_dot_prime=sqrt(Target_X_prime_dot.^2+Target_Y_prime_dot.^2+Target_Z_prime_dot.^2);
            
    [theta,phi,rho] = cart2sph(Target_X_prime, Target_Y_prime,Target_Z_prime);
    
    rho_dot=((Target_X_prime.*Target_X_prime_dot)+(Target_Y_prime.*Target_Y_prime_dot)+(Target_Z_prime.*Target_Z_prime_dot))./(rho);
    denominator_theta=(Target_X_prime.^2+Target_Y_prime.^2);
    numerator_theta=(Target_Y_prime.*Target_X_prime_dot)-(Target_X_prime.*Target_Y_prime_dot);
    theta_dot=(numerator_theta./denominator_theta).*cos(phi);
    
    numerator_phi=Target_Z_prime.*((Target_X_prime.*Target_X_prime_dot)+(Target_Y_prime.*Target_Y_prime_dot));   %The second term in the numerator is zero because Target_Z_prime_dot=0;
    denominator_phi=(rho.^2).*sqrt(denominator_theta);
    phi_dot= numerator_phi./denominator_phi;
    
    TargetVelocityVector=(bsxfun(@hypot, theta_dot, phi_dot))*(180/pi); %Convert to Degrees. 
end



%% The following section includes functions that are being used in the other functions
%but were downloaded from MATLAB central. These functions have been checked
%but the authors bear no responsibility for their accuracy. 

function dx = derivative(x,N,dim)
% DERIVATIVE Compute derivative while preserving dimensions.
% 
% DERIVATIVE(X), for a vector X, is an estimate of the first derivative of X.
% DERIVATIVE(X), for a matrix X, is a matrix containing the first
%   derivatives of the columns of X.
% DERIVATIVE(X,N) is the Nth derivative along the columns of X.
% DERIVATIVE(X,N,DIM) is the Nth derivative along dimension DIM of X. 
% 
% DERIVATIVE averages neighboring values of the simple finite differencing
% method to obtain an estimate of the derivative that is exactly the same
% size as X. This stands in contrast to Matlab's built-in DIFF, which, when
% computing a derivative of order N on length M vectors, produces a vector
% of length M-N. DERIVATIVE is therefore useful for estimating derivatives
% at the same points over which X is defined, rather than in between
% samples (as occurs implicity when using Matlab's DIFF). This means that,
% for example, dX can be plotted against the same independent variables as
% X. Note that the first and last elements of DERIVATIVE(X) will be the
% same as those produced by DIFF(X).
%
% For N > 1, DERIVATIVE operates iteratively N times. If N = 0, DERIVATIVE
% is the identity transformation. Use caution when computing derivatives
% for N high relative to size(X,DIM). A warning will be issued.
% 
% Unless DIM is specified, DERIVATIVE computes the Nth derivative
% along the columns of a matrix input.
%
% EXAMPLE: 
% t = linspace(-4,4,500); x = normpdf(t); 
% dx = derivative(x); dt = derivative(t); 
% plot(t,x,t,dx./dt);
% 
% Created by Scott McKinney, October 2010
%
% See also GRADIENT

%set DIM
if nargin<3  
   if size(x,1)==1 %if row vector        
       dim = 2;
   else
       dim = 1; %default to computing along the columns, unless input is a row vector
   end
else           
    if ~isscalar(dim) || ~ismember(dim,[1 2])    
        error('dim must be 1 or 2!')
    end
end

%set N
if nargin<2 || isempty(N) %allows for letting N = [] as placeholder
    N = 1; %default to first derivative    
else        
    if ~isscalar(N) || N~=round(N)
        error('N must be a scalar integer!')
    end
end

if size(x,dim)<=1 && N
    error('X cannot be singleton along dimension DIM')
elseif N>=size(x,dim)
    warning('Computing derivative of order longer than or equal to size(x,dim). Results may not be valid...')
end

dx = x; %'Zeroth' derivative

for n = 1:N % Apply iteratively

    dif = diff(dx,1,dim);

    if dim==1
        first = [dif(1,:) ; dif];
        last = [dif; dif(end,:)];
    elseif dim==2;
        first = [dif(:,1) dif];
        last = [dif dif(:,end)];
    end
    
    dx = (first+last)/2;
end

end


function hhh=vline(x,in1,in2)
% function h=vline(x, linetype, label)
% 
% Draws a vertical line on the current axes at the location specified by 'x'.  Optional arguments are
% 'linetype' (default is 'r:') and 'label', which applies a text label to the graph near the line.  The
% label appears in the same color as the line.
%
% The line is held on the current axes, and after plotting the line, the function returns the axes to
% its prior hold state.
%
% The HandleVisibility property of the line object is set to "off", so not only does it not appear on
% legends, but it is not findable by using findobj.  Specifying an output argument causes the function to
% return a handle to the line, so it can be manipulated or deleted.  Also, the HandleVisibility can be 
% overridden by setting the root's ShowHiddenHandles property to on.
%
% h = vline(42,'g','The Answer')
%
% returns a handle to a green vertical line on the current axes at x=42, and creates a text object on
% the current axes, close to the line, which reads "The Answer".
%
% vline also supports vector inputs to draw multiple lines at once.  For example,
%
% vline([4 8 12],{'g','r','b'},{'l1','lab2','LABELC'})
%
% draws three lines with the appropriate labels and colors.
% 
% By Brandon Kuczenski for Kensington Labs.
% brandon_kuczenski@kensingtonlabs.com
% 8 November 2001

if length(x)>1  % vector input
    for I=1:length(x)
        switch nargin
        case 1
            linetype='r:';
            label='';
        case 2
            if ~iscell(in1)
                in1={in1};
            end
            if I>length(in1)
                linetype=in1{end};
            else
                linetype=in1{I};
            end
            label='';
        case 3
            if ~iscell(in1)
                in1={in1};
            end
            if ~iscell(in2)
                in2={in2};
            end
            if I>length(in1)
                linetype=in1{end};
            else
                linetype=in1{I};
            end
            if I>length(in2)
                label=in2{end};
            else
                label=in2{I};
            end
        end
        h(I)=vline(x(I),linetype,label);
    end
else
    switch nargin
    case 1
        linetype='r:';
        label='';
    case 2
        linetype=in1;
        label='';
    case 3
        linetype=in1;
        label=in2;
    end

    
    
    
    g=ishold(gca);
    hold on

    y=get(gca,'ylim');
    h=plot([x x],y,linetype);
    if length(label)
        xx=get(gca,'xlim');
        xrange=xx(2)-xx(1);
        xunit=(x-xx(1))/xrange;
        if xunit<0.8
            text(x+0.01*xrange,y(1)+0.1*(y(2)-y(1)),label,'color',get(h,'color'))
        else
            text(x-.05*xrange,y(1)+0.1*(y(2)-y(1)),label,'color',get(h,'color'))
        end
    end     

    if g==0
    hold off
    end
    set(h,'tag','vline','handlevisibility','off')
end % else

if nargout
    hhh=h;
end
end


function hhh=hline(y,in1,in2)
% function h=hline(y, linetype, label)
% 
% Draws a horizontal line on the current axes at the location specified by 'y'.  Optional arguments are
% 'linetype' (default is 'r:') and 'label', which applies a text label to the graph near the line.  The
% label appears in the same color as the line.
%
% The line is held on the current axes, and after plotting the line, the function returns the axes to
% its prior hold state.
%
% The HandleVisibility property of the line object is set to "off", so not only does it not appear on
% legends, but it is not findable by using findobj.  Specifying an output argument causes the function to
% return a handle to the line, so it can be manipulated or deleted.  Also, the HandleVisibility can be 
% overridden by setting the root's ShowHiddenHandles property to on.
%
% h = hline(42,'g','The Answer')
%
% returns a handle to a green horizontal line on the current axes at y=42, and creates a text object on
% the current axes, close to the line, which reads "The Answer".
%
% hline also supports vector inputs to draw multiple lines at once.  For example,
%
% hline([4 8 12],{'g','r','b'},{'l1','lab2','LABELC'})
%
% draws three lines with the appropriate labels and colors.
% 
% By Brandon Kuczenski for Kensington Labs.
% brandon_kuczenski@kensingtonlabs.com
% 8 November 2001

if length(y)>1  % vector input
    for I=1:length(y)
        switch nargin
        case 1
            linetype='r:';
            label='';
        case 2
            if ~iscell(in1)
                in1={in1};
            end
            if I>length(in1)
                linetype=in1{end};
            else
                linetype=in1{I};
            end
            label='';
        case 3
            if ~iscell(in1)
                in1={in1};
            end
            if ~iscell(in2)
                in2={in2};
            end
            if I>length(in1)
                linetype=in1{end};
            else
                linetype=in1{I};
            end
            if I>length(in2)
                label=in2{end};
            else
                label=in2{I};
            end
        end
        h(I)=hline(y(I),linetype,label);
    end
else
    switch nargin
    case 1
        linetype='r:';
        label='';
    case 2
        linetype=in1;
        label='';
    case 3
        linetype=in1;
        label=in2;
    end

    
    
    
    g=ishold(gca);
    hold on

    x=get(gca,'xlim');
    h=plot(x,[y y],linetype);
    if ~isempty(label)
        yy=get(gca,'ylim');
        yrange=yy(2)-yy(1);
        yunit=(y-yy(1))/yrange;
        if yunit<0.2
            text(x(1)+0.02*(x(2)-x(1)),y+0.02*yrange,label,'color',get(h,'color'))
        else
            text(x(1)+0.02*(x(2)-x(1)),y-0.02*yrange,label,'color',get(h,'color'))
        end
    end

    if g==0
    hold off
    end
    set(h,'tag','hline','handlevisibility','off') % this last part is so that it doesn't show up on legends
end % else

if nargout
    hhh=h;
end
end

function [anew,bnew] = accumconncomps(a,b,fun)

% Construct array with accumulation of connected components 
% 
%     [c,valnew] = accumconncomps(cc,val)
%     [c,valnew] = accumconncomps(cc,val,fun)
%     [c,valnew] = accumconncomps(cc)
%
% accumconncomps creates vectors by accumulating elements in val using
% connected components in cc. Connected components are subsequent,
% identical elements in the vector cc.
%
% The input vectors cc and val must have same size. The output array c 
% contains the values of each connected component 
% (e.g. cc=[1 1 2 2 2 1 2 3 3] returns c=[1 2 1 2 3]). valnew contains the
% aggregated values in val in each connected component.
%
% fun is a function handle that determines the aggregation mode (default:
% @sum). fun must be a function that takes a vector and returns a scalar 
% (e.g. @mean, @var, @(x) max(x)-min(x)).
%
% accumconncomps(subs) is an equal expression to 
% accumconncomps(subs,ones(size(subs)),@sum) and counts the number of
% elements in each connected component.
%
% Example 1:
%
% Sum the values in val according to the connected components in cc.
%
%     cc  = [1 1 2 1 1 1 3 3 3 4 2 2];
%     val = [2.3 1.2 5 3 2 5 3.2 4.5 2 2.2 1.2 2.2];
% 
%     [c,valnew] = accumconncomps(cc,val,@sum)
% 
%     c    =
% 
%          1     2     1     3     4     2
% 
%     valnew =
% 
%          3.5   5.0   10.0  9.7   2.2   3.4
%
%
% Example 2:
%
% What does a distribution of the lengths of connected components in a
% random sequence of zeros and ones look like?
%
%    cc  = round(rand(1000000,1));
%    [c,valnew] = accumconncomps(cc);
%    hist(valnew,20)
%
%
% See also: ACCUMARRAY
%
% Author: Wolfgang Schwanghart (w.schwanghart[at]unibas.ch)
% Date: 10. Sept. 2008


% check input arguments
if nargin == 1
    b   = ones(size(a));
    fun = @sum;
elseif nargin == 2
    fun = @sum;
elseif nargin == 3
    % check if functionhandle is provided
    if ~isa(fun,'function_handle')
        error('the third input argument must be a function handle')
    end
else
    error('wrong number of input arguments')
end

% are vectors provided?
if ~isvector(a)
    error('val and subs must be vectors')
end

% do they have the same size?
siza = size(a);
sizb = size(b);
if siza~= sizb;
    error('val and subs must have same size')
end

% transpose if both vectors are row vectors
if siza(1)<siza(2)
    a = a(:);
    b = b(:);
    flagtranspose = true;
else
    flagtranspose = false;
end

% find beginnings of connected components
ad = [true; diff(a)~=0];

% assign new subs to the vector 
adc = cumsum(ad);

% nr of independent layers
uniqueLayers = adc(end);

% use accumarray to construct new vector
bnew = accumarray(adc,b,[uniqueLayers 1],fun);
anew = a(ad);

% transpose back if row vectors were provided
if flagtranspose
    anew = anew';
    bnew = bnew';
end
end


by=byss;
vp=1;                % Price dispersion
tauc=taucss;           % Consumption tax- https://www.oecd.org/en/publications/consumption-tax-trends-2024_dcd4dd36-en.html#:~:text=Standard%20VAT%20rates%20across%20OECD,to%208.1%25%20in%202024).
tauw =tauwss;          % Income tax: https://www.oecd.org/content/dam/oecd/en/topics/policy-issues/tax-policy/taxing-wages-united-states.pdf
PIstar=1;            % Optimnal gross inflation
PI=1;                % Gross inflation
R=g/betta;  % interest rate
rk=g/betta-(1-delta);   % return on private investment
%(R/g-1)*400
N=1/3;                    % Effective Labor supply
%H=1;
%L=0.2;
%E=0.1;


%eff=effss;
%effge=effgess;
% Marginal cost
mc=(epsilon-1)/epsilon;

%kG_y=eff*Igiy/(1-(1-delta)/g);
kG_y=(1-eGI_ss)*Igiy/(g-(1-delta));

Kp_y=alpha*mc/(markupss*rk);

yt_proxy=(kG_y^alphaG)*(Kp_y^alpha)*(N^(1-alpha));

y=yt_proxy^(1/(1-alphaG-alpha));


w=(1-alpha)*mc*y/N/markupss;

%Kp=alpha/(1-alpha)*w/rk*g*N;

% Private capital
Kp=alpha/(1-alpha)*w/rk*N;

% Private investment
Ip=Kp*(g-(1-delta));

% Public capital
Kg=kG_y*y;

% NEW PATH
%kGe_y=effge*Igey/(1-(1-delta)/g);
% Human capital
%kGe_y=effge*Igey/(g-(1-delta));
kGe_y=(1-eGE_ss)*Igey/(g-(1-delta));
Kge=kGe_y*y;
Ige=Igey*y;
Grd=Grdy*y;




% R&D path
%markupss=1.015;
A=1;
q=qss;
SDF=betta;
V=(1+gammaa)/(1+gammaa-phi*SDF)*(markupss-1)/(markupss/mc)*y;
Z=(1+gammaa-phi)/(q*phi)+A;

J=(1-varsigma)*q*phi*SDF/(1+gammaa-(1-q+varsigma*q)*phi*betta)*V;

S=varsigma*q*phi*SDF/(1+gammaa)*(V-J);

%Srd=SDF*J*(Z/A-phi*Z/A*1/(1+gammaa));
%shockchi=(1+gammaa-phi)/(Srd^alphaHA*Grd^alphaRD);
%shockchi=(1+gammaa-phi)/(Srd^alphaHA);



kappaprob=q/((S)^varsigma);




share_in_RD=((Z/A-1)*S)/y;
(Z/A-1)*S/y
Ip_y=Ip/y;
%Ip_y=(1-(1-delta)/g)*Kp_y;
Ip_y=(g-(1-delta))*Kp_y;

Rss=R;
ydss=y;

yd=y;
Igi=Igiy*y;
Gc=Gcy*y;

C=yd-(Ip+Igi+Gc+Ige+Grd+(Z/A-1)*S);
lambda=1/C/(1+tauc);

Cy=1-Ip_y-Igiy-Gcy-Igey-Grdy-((Z/A-1)*S)/yd;
x2=1/(1+tauc)*1/Cy/(1-betta*thetap);  % x2=lambda*y/(1-betta*thetap)= 1/(1+tauc)*y/c/(1-betta*thetap)
x1=mc*x2;

b=y*by;
T=b-((R/PI)*b/g+Gc+Igi+Ige+Grd-tauw*w*N-tauc*C);

%Variables of interest
G=Gc+Igi+Ige+Grd;
rreal=R/PI;
pdef_yss=(Gc+Igi+Ige+Grd+T-tauw*w*N-tauc*C)/ydss;
T_yss=T/ydss;
by_yss=b/ydss;



L=N;

%{
Lss=0.3
Ess=0.05
muySS=(1/betta-1+deltaH)/(Lss/Ess)/deltaH
%}

Lab_E_ratio=(1/betta-1+deltaH)/(gamma*deltaH);
E=L/Lab_E_ratio;
% Langangra of teh human capital equation
lambda_H=lambda*w*(1-tauw)/(gamma*1/E*deltaH);

% L
%L=lambda_H*(1/betta-1+deltaH)/(lambda*(1-tauw)*w);
%deltaH=0.016
%
% Human capital
%H=N/L;
H=N/L;

% Adjustment parameter for N
omega=lambda*w*(1-tauw)*H/(L+E)^varphi;

chiH=omega*(L+E)^varphi/(lambda_H*gamma*E^(gamma-1)* (Kge)^mu);


eGE=eGE_ss;
eGI=eGI_ss;


eGRD=eGRD_ss;
%A=1;

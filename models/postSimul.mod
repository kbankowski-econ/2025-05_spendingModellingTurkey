perfect_foresight_setup(periods=2000);
perfect_foresight_solver(maxit=20);

fiscalchange=(Igi-Igi(1))+(Ige-Ige(1))+(Grd-Grd(1));
% Period 1 is the pre-shock steady state (the baseline, subtracted as yd(1));
% the shock is active from period 2 on. An N-year horizon is the 4N quarters in
% indices 2:(N*4+1), so ped=N*4+1 (the slice 2:ped is inclusive of both ends).
ped=1*4+1;
multiplier_1y=sum((yd(2:ped)-yd(1)))/sum((fiscalchange(2:ped)))
ped=5*4+1;
multiplier_5y=sum((yd(2:ped)-yd(1)))/sum((fiscalchange(2:ped)))
ped=10*4+1;
multiplier_10y=sum((yd(2:ped)-yd(1)))/sum((fiscalchange(2:ped)))
ped=20*4+1;
multiplier_20y=sum((yd(2:ped)-yd(1)))/sum((fiscalchange(2:ped)))
ped=25*4+1;
multiplier_25y=sum((yd(2:ped)-yd(1)))/sum((fiscalchange(2:ped)))

within ;
model SimpleRC_Input
  "A simple thermal R1C1 model with sinusoidal outside air temperature and heating input."
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor cap(C=1e6)
    annotation (Placement(transformation(extent={{10,0},{30,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor res(R=0.01)
    annotation (Placement(transformation(extent={{-20,-10},{0,10}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor senTZone
    annotation (Placement(transformation(extent={{40,-10},{60,10}})));
  Modelica.Blocks.Interfaces.RealOutput TZone
    "Zone air temperature measurement"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTOut
    annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
  Modelica.Blocks.Sources.Sine souTOut(
    freqHz=1/(3600*24),
    offset=273.15 + 20,
    amplitude=10)
    annotation (Placement(transformation(extent={{-100,-10},{-80,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
    annotation (Placement(transformation(extent={{0,-60},{20,-40}})));
  Modelica.Blocks.Math.Gain eff(k=1/0.99)
    annotation (Placement(transformation(extent={{0,-80},{20,-60}})));
  Modelica.Blocks.Interfaces.RealOutput PHeat "Power consumption of heater"
    annotation (Placement(transformation(extent={{100,-70},{120,-50}})));
  Modelica.Blocks.Interfaces.RealOutput EHeat "Energy consumption of heater"
    annotation (Placement(transformation(extent={{100,-90},{120,-70}})));
  Modelica.Blocks.Continuous.Integrator intEHeat(initType=Modelica.Blocks.Types.Init.InitialState,
      y_start=0)
    annotation (Placement(transformation(extent={{60,-90},{80,-70}})));
  Modelica.Blocks.Sources.Constant
                               setpoint(k=20 + 273.15)
    annotation (Placement(transformation(extent={{-130,-60},{-110,-40}})));
  IBPSA.Controls.Continuous.LimPID conPID(
    controllerType=Modelica.Blocks.Types.SimpleController.P,
    k=2000,
    yMax=10000)
    annotation (Placement(transformation(extent={{-60,-40},{-40,-60}})));
  inner IBPSA.Utilities.IO.RESTClient.Configuration config
    annotation (Placement(transformation(extent={{80,80},{100,100}})));
  IBPSA.Utilities.IO.RESTClient.Read_Real acs_Setpoint(
    numVar=1,
    activation=IBPSA.Utilities.IO.RESTClient.Types.LocalActivation.use_input,
    varName={"SetHeat"},
    t0=0,
    threshold=-1,
    hostAddress="127.0.0.1",
    tcpPort=8888)
    annotation (Placement(transformation(extent={{-92,-60},{-72,-40}})));
  IBPSA.Utilities.IO.RESTClient.Read_Real acs_Actuator(
    numVar=1,
    varName={"QHeat"},
    threshold=-1,
    hostAddress="127.0.0.1",
    tcpPort=8888,
    activation=IBPSA.Utilities.IO.RESTClient.Types.LocalActivation.use_activation,

    t0=0.1)
    annotation (Placement(transformation(extent={{-30,-60},{-10,-40}})));
  Modelica.Blocks.Sources.BooleanConstant booleanConstant(k=false)
    annotation (Placement(transformation(extent={{-100,40},{-80,60}})));
  IBPSA.Utilities.IO.RESTClient.Send_Real sen_TZone(
    numVar=1,
    varName={"TZone"},
    t0=0,
    hostAddress="127.0.0.1",
    tcpPort=8888)
          annotation (Placement(transformation(extent={{90,20},{110,40}})));
equation
  connect(res.port_b, cap.port)
    annotation (Line(points={{0,0},{20,0}}, color={191,0,0}));
  connect(cap.port, senTZone.port)
    annotation (Line(points={{20,0},{40,0}}, color={191,0,0}));
  connect(senTZone.T, TZone)
    annotation (Line(points={{60,0},{110,0}}, color={0,0,127}));
  connect(preTOut.port, res.port_a)
    annotation (Line(points={{-40,0},{-20,0}}, color={191,0,0}));
  connect(souTOut.y, preTOut.T)
    annotation (Line(points={{-79,0},{-62,0}}, color={0,0,127}));
  connect(preHeat.port, cap.port)
    annotation (Line(points={{20,-50},{20,0}},           color={191,0,0}));
  connect(eff.y, PHeat) annotation (Line(points={{21,-70},{40,-70},{40,-60},{
          110,-60}}, color={0,0,127}));
  connect(intEHeat.y,EHeat)
    annotation (Line(points={{81,-80},{110,-80}}, color={0,0,127}));
  connect(intEHeat.u, PHeat) annotation (Line(points={{58,-80},{40,-80},{40,-70},
          {40,-70},{40,-60},{110,-60}}, color={0,0,127}));
  connect(eff.u, preHeat.Q_flow) annotation (Line(points={{-2,-70},{-6,-70},{-6,
          -50},{0,-50}}, color={0,0,127}));
  connect(conPID.u_m, TZone) annotation (Line(points={{-50,-38},{-50,-28},{80,
          -28},{80,0},{110,0}}, color={0,0,127}));
  connect(setpoint.y, acs_Setpoint.u[1])
    annotation (Line(points={{-109,-50},{-94,-50}}, color={0,0,127}));
  connect(acs_Setpoint.y[1], conPID.u_s)
    annotation (Line(points={{-70.6,-50},{-62,-50}}, color={0,0,127}));
  connect(conPID.y,acs_Actuator. u[1])
    annotation (Line(points={{-39,-50},{-32,-50}}, color={0,0,127}));
  connect(acs_Actuator.y[1], preHeat.Q_flow)
    annotation (Line(points={{-8.6,-50},{0,-50}}, color={0,0,127}));
  connect(booleanConstant.y, acs_Setpoint.activate) annotation (Line(points={{
          -79,50},{-74,50},{-74,26},{-106,26},{-106,-42},{-94,-42}}, color={255,
          0,255}));
  connect(sen_TZone.u[1], senTZone.T)
    annotation (Line(points={{88,30},{80,30},{80,0},{60,0}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.2"),
      IBPSA(version="2.0.0"),
      Buildings(version="6.0.0")), experiment(StopTime=86400, Interval=300));
end SimpleRC_Input;

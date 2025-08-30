create table tmp_ads_spend (
  date date, 
  platform varchar(100), 
  account varchar(100), 
  campaign varchar(100), 
  country varchar(100), 
  device varchar(100), 
  spend numeric(10,2), 
  clicks numeric(10), 
  impressions numeric(10), 
  conversions numeric(10), 
  load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  source_file varchar(100), 
  status varchar(1) default 'C');

  create table ads_spend_data (
  date date, 
  platform varchar(100), 
  account varchar(100), 
  campaign varchar(100), 
  country varchar(100), 
  device varchar(100), 
  spend numeric(10,2), 
  clicks numeric(10), 
  impressions numeric(10), 
  conversions numeric(10), 
  load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  source_file varchar(100));
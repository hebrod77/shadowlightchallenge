create table kpi_model as
with max_date as (
  select max(date) as max_date from tmp_ads_spend
), 

last_30_days as (
select platform, account, campaign, country, device, sum(spend) spend, sum(clicks) clicks, sum(impressions) impressions, sum(conversions) conversions, round(sum(spend)/sum(conversions),2) as CAC, round(sum(conversions) * 100 / sum(spend),2) as ROAS 
from tmp_ads_spend, max_date
where date between max_date - 30 and max_date
group by platform, account, campaign, country, device)

, previous_30_days as (
select platform, account, campaign, country, device, sum(spend) spend, sum(clicks) clicks, sum(impressions) impressions, sum(conversions) conversions, round(sum(spend)/sum(conversions),2) as CAC, round(sum(conversions) * 100 / sum(spend),2) as ROAS 
from tmp_ads_spend, max_date
where date between max_date - 60 and max_date - 30
group by platform, account, campaign, country, device)

select l30.platform, l30.account, l30.campaign, l30.country, l30.device, 
l30.spend spend_last_30, p30.spend spend_previous30, round((l30.spend - p30.spend)/p30.spend*100,2) spend_delta_percentage, 
l30.clicks clicks_last_30, p30.clicks clicks_previous30, round((l30.clicks - p30.clicks)/p30.clicks*100,2) clicks_delta_percentage, 
l30.impressions impressions_last_30, p30.impressions impressions_previous30, round((l30.impressions - p30.impressions)/p30.impressions*100,2) impressions_delta_percentage, 
l30.conversions conversions_last_30, p30.conversions conversions_previous30, round((l30.conversions - p30.conversions)/p30.conversions*100,2) conversions_delta_percentage,
l30.CAC CAC_last_30, p30.CAC CAC_previous30, round((l30.CAC - p30.CAC)/p30.CAC*100,2) CAC_delta_percentage, 
l30.ROAS ROAS_last_30, p30.ROAS ROAS_previous30, round((l30.ROAS - p30.ROAS)/p30.ROAS*100,2) ROAS_delta_percentage
from last_30_days l30
inner join previous_30_days p30 on l30.platform = p30.platform and l30.account = p30.account and l30.campaign = p30.campaign and l30.country = p30.country and l30.device = p30.device

union all

select l30.platform, l30.account, l30.campaign, l30.country, l30.device, 
l30.spend spend_last_30, null spend_previous30, null spend_delta_percentage, 
l30.clicks clicks_last_30, null clicks_previous30, null clicks_delta_percentage, 
l30.impressions impressions_last_30, null impressions_previous30, null impressions_delta_percentage, 
l30.conversions conversions_last_30, null conversions_previous30, null conversions_delta_percentage,
l30.CAC CAC_last_30, null CAC_previous30, null CAC_delta_percentage, 
l30.ROAS ROAS_last_30, null ROAS_previous30, null ROAS_delta_percentage
from last_30_days l30
where not exists (select 1 from previous_30_days p30 
where l30.platform = p30.platform and l30.account = p30.account and l30.campaign = p30.campaign and l30.country = p30.country and l30.device = p30.device)

union all

select p30.platform, p30.account, p30.campaign, p30.country, p30.device, 
null spend_last_30, p30.spend spend_previous30, null spend_delta_percentage, 
null clicks_last_30, p30.clicks clicks_previous30, null clicks_delta_percentage, 
null impressions_last_30, p30.impressions impressions_previous30, null impressions_delta_percentage, 
null conversions_last_30, p30.conversions conversions_previous30, null conversions_delta_percentage,
null CAC_last_30, p30.CAC CAC_previous30, null CAC_delta_percentage, 
null ROAS_last_30, p30.ROAS ROAS_previous30, null ROAS_delta_percentage
from previous_30_days p30
where not exists (select 1 from last_30_days l30
where l30.platform = p30.platform and l30.account = p30.account and l30.campaign = p30.campaign and l30.country = p30.country and l30.device = p30.device);
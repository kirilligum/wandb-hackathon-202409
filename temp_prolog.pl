% companies
company(canva).
company(weights_biases).

% products and services
product_service(ml_platform).
product_service(model_registry).
product_service(online_design_tool).
product_service(ai_tools).
product_service(experiment_tracking).

% customers
customer(thibault_main_de_boissiere).

% customer segments
customer_segment(ml_engineers).
customer_segment(product_managers).

% marketing campaigns
marketing_campaign(ml_workflow_improvement).

% sales representatives
sales_representative(thibault_main_de_boissiere).

% marketing channels
marketing_channel(digital_marketing).
marketing_channel(trade_shows).
marketing_channel(email_campaigns).

% competitors
competitor(adobe).
competitor(google).

% partners and suppliers
partner_supplier(anyscale).
partner_supplier(amazon).

% market segments
market_segment(enterprise_software).
market_segment(ai_tools).

% events and conferences
event(ml_conference_2023).

% trends and technologies
trend_technology(ml_operations).
trend_technology(generative_models).
trend_technology(personalization).

% geographic locations
geographic_location(global).
geographic_location(remote).

% connections
offers(canva, online_design_tool).
offers(canva, ai_tools).
offers(weights_biases, experiment_tracking).
purchases(thibault_main_de_boissiere, model_registry).
located_in(canva, geographic_location(global)).
located_in(thibault_main_de_boissiere, geographic_location(remote)).
targets(ml_workflow_improvement, customer_segment(ml_engineers)).
utilizes(ml_workflow_improvement, marketing_channel(digital_marketing)).
competes_with(canva, competitor(adobe)).
competes_with(canva, competitor(google)).
partners_with(canva, partner_supplier(anyscale)).
partners_with(canva, partner_supplier(amazon)).
belongs_to(thibault_main_de_boissiere, market_segment(enterprise_software)).
attended_by(ml_conference_2023, canva).
attended_by(ml_conference_2023, thibault_main_de_boissiere).
influences(trend_technology(ml_operations), market_segment(enterprise_software)).
managed_by(sales_representative(thibault_main_de_boissiere), ml_platform).
interacts_on(thibault_main_de_boissiere, social_media_platform(linkedin)).
associated_with(product_service(model_registry), trend_technology(ml_operations)).
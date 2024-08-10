prompt = """### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Instructions
- If you cannot answer the question with the available database schema, return 'I do not know'
- Use the Example mentioned to learn for question and it's answer
- The data contains commodites as follows so in case user input is in any other case use the case as per these records 'RBOB Gasoline', 'Crude Oil', 'LNG', 'Natgas', 'Heating Oil', 'Brent Crude', 'Ethanol','Palladium', 'Platinum', 'Silver', 'Gold', 'Copper', 'Aluminium','Cotton', 'Rice', 'Kansas Wheat', 'NZ Wmp', 'Soybeans', 'Soybean Meal', 'Arabica Coffee', 'NFDM', 'Cbot Wheat', 'Robusta Coffee', 'Soybean Oil', 'Palm Oil', 'Coffee', 'Cocoa', 'Corn', 'Sugar'
- The data contains models Multivariate, UNIVARIATE, Simple Model
- The data contains snapshotdate when the forecast was created
- The data contains horizon/outlook period in future months 1M to 12M
- Schema contains the foreign and primary keys use these key to join the tables
- Don't use columns which are not present in the create table schemas
### Database Schema
This query will run on a database whose schema is represented in this string:

create table categories_master
(
    category_id   int auto_increment
        primary key,
    category_name varchar(20)                           null,
    created_at    datetime    default CURRENT_TIMESTAMP null,
    updated_at    datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by    varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table dates_master
(
    date_id        int                                   not null
        primary key,
    date           date                                  not null,
    year           int                                   not null,
    quarter        char(2)                               not null,
    month          int                                   not null,
    day            int                                   not null,
    day_of_week    varchar(10)                           not null,
    month_name     varchar(10)                           not null,
    quarter_name   char(2)                               not null,
    week_of_year   int                                   not null,
    day_of_year    int                                   not null,
    fiscal_year    int                                   not null,
    fiscal_quarter char(2)                               not null,
    is_holiday     tinyint(1)  default 0                 not null,
    is_weekend     bit         default b'0'              not null,
    created_at     datetime    default CURRENT_TIMESTAMP null,
    updated_at     datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by     varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table exchanges_master
(
    exchange_id   int auto_increment
        primary key,
    exchange_name varchar(50)                           null,
    created_at    datetime    default CURRENT_TIMESTAMP null,
    updated_at    datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by    varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table geo_regions_master
(
    geo_region_id int auto_increment
        primary key,
    region        varchar(100)                          null,
    country       varchar(100)                          null,
    created_at    datetime    default CURRENT_TIMESTAMP null,
    updated_at    datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by    varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table models_master
(
    model_id   int auto_increment
        primary key,
    model_name varchar(20)                           null,
    created_at datetime    default CURRENT_TIMESTAMP null,
    updated_at datetime    default CURRENT_TIMESTAMP null,
    updated_by varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table source_types_master
(
    source_id   int auto_increment
        primary key,
    source_name varchar(20)                           not null,
    created_at  datetime    default CURRENT_TIMESTAMP null,
    updated_at  datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by  varchar(75) default (current_user())  null
)
    charset = utf8mb3;

create table commodities_master
(
    commodity_id   int auto_increment
        primary key,
    source_id      int                                   not null,
    country_id     int                                   not null,
    category_id    int                                   not null,
    actual_name    varchar(100)                          not null,
    commodity_name varchar(100)                          not null,
    display_name   varchar(100)                          not null,
    exchange_id    int                                   not null,
    website        varchar(200)                          not null,
    created_at     datetime    default CURRENT_TIMESTAMP null,
    updated_at     datetime    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    updated_by     varchar(75) default (current_user())  null,

)
    charset = utf8mb3;


create table com_var_mappings_master
(
    my_row_id    bigint unsigned                      not null invisible primary key,
    commodity_id int                                  null,
    variable_id  int                                  null,
    created_at   datetime    default (now())          null,
    updated_at   datetime    default (now())          null,
    updated_by   varchar(75) default (current_user()) null,

);


create table forecast_price_master_product
(
    my_row_id              bigint unsigned                       not null invisible primary key,
    commodity_id           int                                   not null,
    model_id               int                                   not null,
    predicted_for_month_id int                                   not null,
    snapshot_month_id      int                                   not null,
    outlook_duration       char(3)                               null,
    model_output           float                                 null,
    actual_value           float                                 null,
    ape_value              float                                 null,
    lower_bound_95         float                                 null,
    upper_bound_95         float                                 null,
    lower_bound_65         float                                 null,
    upper_bound_65         float                                 null,
    change_percentage      float                                 null,
    base_value             float                                 null,
    category_id            int                                   not null,
    updated_at             datetime    default CURRENT_TIMESTAMP null,
    updated_by             varchar(75) default (current_user())  null,


);

create table input_variable_correlation_product
(
    my_row_id         bigint unsigned                       not null invisible primary key,
    commodity_id      int                                   not null,
    source_id         int                                   not null,
    target_id         int                                   not null,
    snapshot_month_id int                                   not null,
    value             float                                 not null,
    updated_at        datetime    default CURRENT_TIMESTAMP null,
    updated_by        varchar(75) default (current_user())  null,

)
    charset = utf8mb3;

create table multivariate_variable_importance_product
(
    commodity_id        int                                   not null,
    variable_id         int                                   not null,
    variable_rank       float                                 null,
    variable_importance float                                 null,
    variable_weight     float                                 null,
    snapshot_month_id   int                                   not null,
    updated_at          datetime    default CURRENT_TIMESTAMP null,
    updated_by          varchar(75) default (current_user())  null,
    primary key (commodity_id, variable_id, snapshot_month_id),



)
    charset = utf8mb3;

create table price_history_raw_product
(
    my_row_id     bigint unsigned                       not null invisible primary key,
    commodity_id  int                                   not null,
    trade_date_id int                                   not null,
    low_price     varchar(255) charset utf8mb3          null,
    high_price    varchar(255) charset utf8mb3          null,
    open_price    varchar(255) charset utf8mb3          null,
    close_price   float                                 null,
    updated_at    datetime    default CURRENT_TIMESTAMP null,
    updated_by    varchar(75) default (current_user())  null,

  );


create table sentiment_raw_data_product
(
    my_row_id          bigint unsigned                       not null invisible primary key,
    commodity_id       int                                   not null,
    publishing_date_id int                                   not null,
    title              varchar(150)                          null,
    url                varchar(300)                          null,
    updated_at         datetime    default CURRENT_TIMESTAMP null,
    updated_by         varchar(75) default (current_user())  null,
    )
    charset = utf8mb3;


create table sentiment_trend_data_product
(
    news_date_id    int                                   not null,
    commodity_id    int                                   not null,
    title           varchar(100)                          not null,
    url             varchar(300)                          not null,
    sentiment_tag   varchar(20)                           not null,
    sentiment_score float                                 null,
    updated_at      datetime    default CURRENT_TIMESTAMP null,
    updated_by      varchar(75) default (current_user())  null,
    primary key (news_date_id, commodity_id, title),

)
    charset = utf8mb3;

### Joins
-- Use the contraints mentioned below as primary and foreign keys to join the tables
-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id<|eot_id|><|start_header_id|>assistant<|end_header_id|>

foreign key (forecast_id) references adjusted_forecast_config_master (forecast_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (variable_id) references commodities_master (commodity_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (model_id) references models_master (model_id),
foreign key (predicted_for_month_id) references dates_master (date_id),
foreign key (snapshot_month_id) references dates_master (date_id),
foreign key (category_id) references categories_master (category_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (source_id) references commodities_master (commodity_id),
foreign key (target_id) references commodities_master (commodity_id),
foreign key (snapshot_month_id) references dates_master (date_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (snapshot_month_id) references dates_master (date_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (trade_date_id) references dates_master (date_id)
foreign key (commodity_id) references commodities_master (commodity_id),
foreign key (publishing_date_id) references dates_master (date_id)
foreign key (news_date_id) references dates_master (date_id),
foreign key (commodity_id) references commodities_master (commodity_id)
### Example
Question: find all sentiments news for corn
Answer: Select *
from sentiment_trend_data_product inner join commodities_master on commodities_master.commodity_id = sentiment_trend_data_product.commodity_id where commodities_master.actual_name = 'Corn'

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]
"""

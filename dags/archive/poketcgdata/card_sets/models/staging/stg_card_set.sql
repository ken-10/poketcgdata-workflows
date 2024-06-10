with source as (
    select
        cs.raw_json ->>'id' as id,
        cs.raw_json ->>'name' as set_name,
        cs.raw_json ->>'total' as total,
        cs.raw_json ->>'series' as series,
        cs.raw_json ->>'printedTotal' as printed_total,
        (cs.raw_json ->>'releaseDate') as release_date,
        (cs.raw_json ->>'updatedAt') as api_updated_datetime,
        (cs.raw_json ->>'images')::json ->> 'logo' as logo_img_url,
        (cs.raw_json ->>'images')::json ->> 'symbol' as symbol_img_url
    from cards.card_set_ldg cs

),
converted as (
    select
        id::varchar as id,
        set_name::varchar as set_name,
        total::int as total,
        series::varchar as series,
        printed_total::int as printed_total,
        release_date::date as release_date,
        api_updated_datetime::timestamp as api_updated_datetime,
        logo_img_url,
        symbol_img_url
    from source
)

select
    id,
    set_name,
    total,
    series,
    printed_total,
    release_date,
    api_updated_datetime,
    logo_img_url,
    symbol_img_url
from converted
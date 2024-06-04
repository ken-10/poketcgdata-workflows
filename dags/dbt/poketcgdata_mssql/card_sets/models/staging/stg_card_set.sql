with source as (
    select
        json_value(lcs.raw_json, '$.id') as id,
        json_value(lcs.raw_json, '$.name') as set_name,
        json_value(lcs.raw_json, '$.total') as total,
        json_value(lcs.raw_json, '$.series') as series,
        json_value(lcs.raw_json, '$.printedTotal') as printed_total,
        json_value(lcs.raw_json, '$.releaseDate') as release_date,
        json_value(lcs.raw_json, '$.updatedAt') as api_updated_datetime,
        json_value(lcs.raw_json, '$.images.logo') as logo_img_url,
        json_value(lcs.raw_json, '$.images.symbol') as symbol_img_url
    from cards.ldg_card_set lcs
)
select
    id as id,
    set_name as set_name,
    cast(total as int) as total,
    series as series,
    cast(printed_total as int) as printed_total,
    cast(release_date as date) as release_date,
    cast(api_updated_datetime as datetime) as api_updated_datetime,
    logo_img_url,
    symbol_img_url
from source

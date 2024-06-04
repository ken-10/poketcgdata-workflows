with source as (
    select
        json_value(lcp.raw_json, '$.id') as card_id,
        json_value(lcp.raw_json, '$.tcgplayer.url') as tcgplayer_url,
        json_value(lcp.raw_json, '$.tcgplayer.updatedAt') as tcgplayer_updated_date,
        json_query(lcp.raw_json, '$.tcgplayer.prices') as prices
    from cards.ldg_card_price lcp
),
parsed_by_card_print as (
    select
        s.card_id,
        s.tcgplayer_url,
        cast(s.tcgplayer_updated_date as date) as tcgplayer_updated_date,
        card_print.[Key] as card_print,
        card_print.[Value] as card_print_prices
    from source s
    cross apply openjson(s.prices, '$') as card_print
)
select
    pbcp.card_id as card_id,
    pbcp.tcgplayer_url as tcgplayer_url,
    pbcp.tcgplayer_updated_date as tcgplayer_updated_date,
    pbcp.card_print as card_print,
    cast(json_value(pbcp.card_print_prices, '$.low') as numeric(15,3)) as low,
    cast(json_value(pbcp.card_print_prices, '$.mid') as numeric(15,3)) as mid,
    cast(json_value(pbcp.card_print_prices, '$.high') as numeric(15,3)) as high,
    cast(json_value(pbcp.card_print_prices, '$.market') as numeric(15,3)) as market,
    cast(json_value(pbcp.card_print_prices, '$.directLow') as numeric(15,3)) as direct_low
from parsed_by_card_print pbcp
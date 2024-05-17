{{
    config(
        materialized='incremental'
    )
}}

select
    stp.card_id as card_id,
    stp.tcgplayer_url as tcgplayer_url,
	stp.tcgplayer_updated_date as tcgplayer_updated_date,
	stp.card_print as card_print,
	stp.low as low,
	stp.mid as mid,
	stp.high as high,
	stp.market as market,
	stp.direct_low as direct_low,
	now() at time zone 'utc' as created_datetime,
	(select id from cards.currency_code where code = 'USD') as currency_cd
from {{ ref('stg_tcgplayer_price') }} stp
    {% if is_incremental() %}
    where stp.tcgplayer_updated_date > (
        select coalesce(max(tp.tcgplayer_updated_date), '1900-01-01')
        from {{ this }} tp
        where stp.card_id = tp.card_id
    )
    {% endif %}
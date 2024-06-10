with source as (
	select
		cpl.raw_json ->> 'id' as card_id,
		(cpl.raw_json ->> 'tcgplayer')::json ->> 'url' as tcgplayer_url,
		(cpl.raw_json ->> 'tcgplayer')::json ->> 'updatedAt' as tcgplayer_updated_date,
		(cpl.raw_json ->> 'tcgplayer')::json ->> 'prices' as prices
	from cards.card_price_ldg cpl
),
extracted_card_print as (
	select
	    s.card_id,
	    s.tcgplayer_url,
	    s.tcgplayer_updated_date,
	    je.key as card_print,
	    je.value as prices
	from source s
	join json_each(s.prices::json) je on true
)
select
	ecp.card_id::varchar as card_id,
	ecp.tcgplayer_url::varchar as tcgplayer_url,
	ecp.tcgplayer_updated_date::date as tcgplayer_updated_date,
	ecp.card_print::varchar as card_print,
	(ecp.prices ->> 'low')::numeric(15,3) as low,
	(ecp.prices ->> 'mid')::numeric(15,3) as mid,
	(ecp.prices ->> 'high')::numeric(15,3) as high,
	(ecp.prices ->> 'market')::numeric(15,3) as market,
	(ecp.prices ->> 'directLow')::numeric(15,3) as direct_low
from extracted_card_print ecp

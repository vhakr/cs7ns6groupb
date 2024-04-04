#!/bin/bash
clear -x
h=localhost
p=5000

get() {
	echo $@
	2>/dev/null curl "$h:$p$1" | cat
	echo -e "\n"
}

get "/customer/create?customer=neimhin&pwd=pwd&tenant_id=eur"

get "/family/create?customer=neimhin&pwd=pwd&tenant_id=eur&family_id=0"

get "/customer/create?customer=cian&pwd=pwd&tenant_id=eur"

get "/family/join?customer=cian&pwd=pwd&family_tenant_id=eur&family_id=0"

get "/family/purchase?customer=cian&pwd=pwd&till=TODO&till_pwd=TODO&amount_euro_equivalent=10"

get "/family/voucher?till=till&till_pwd=till_pwd&customer=cian&pwd=pwd&subtotal=40"

sleep 6

get "/family/voucher?till=till&till_pwd=till_pwd&customer=cian&pwd=pwd&subtotal=40"

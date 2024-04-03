#!/bin/bash
clear -x
h=localhost
p=5000

get() {
	echo $@
	2>/dev/null curl "$h:$p$1" | cat
	echo -e "\n"
}

get "/customer/create?customer=neimhin&pwd=pwd&tenant_id=0"

get "/family/create?customer=neimhin&pwd=pwd&tenant_id=0&family_id=0"

get "/customer/create?customer=cian&pwd=pwd&tenant_id=0"

get "/family/join?customer=cian&pwd=pwd&family_tenant_id=0&family_id=0"

get "/family/purchase?customer=cian&pwd=pwd&till=TODO&till_pwd=TODO&amount_euro_equivalent=10"

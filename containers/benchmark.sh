#!/bin/bash
clear -x
h=localhost
p=80

get() {
	echo $@
	2>/dev/null curl "$h:$p$1" | cat
	echo -e "\n"
}
regions=$@
if [ -z "$regions" ]; then
	regions=eur
fi

for region in $regions; do
	for _ in {1..100}; do
		# get "/customer/create?customer=neimhin&pwd=pwd&tenant_id=$region&pwd=pass" &
		# get "/family/create?customer=neimhin&pwd=pwd&tenant_id=$region&family_id=0" &
		# get "/family/join?customer=cian&pwd=pwd&family_tenant_id=$region&family_id=0" &
		# get "/family/purchase?customer=cian&pwd=pwd&till=TODO&till_pwd=TODO&amount_euro_equivalent=10" &
		get "/family/voucher?till=till&till_pwd=till_pwd&customer=neimhin&pwd=pass&subtotal=40" &
	done

	wait
	echo "Done"
	
done

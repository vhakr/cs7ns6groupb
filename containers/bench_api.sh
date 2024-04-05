
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

for i in `seq 1 100`; do
	region=eur
	get "/customer/create?customer=neimhin&pwd=pwd&tenant_id=$region" &
done

wait
echo hello

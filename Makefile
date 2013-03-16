init:
	@makemkdir -p archive/$(ACCOUNT)/
	@scripts/init.py $(ACCOUNT) > archive/$(ACCOUNT)/tmp
	@make append ACCOUNT=$(ACCOUNT)

fetch:
	@$(eval ID:=$(shell cat archive/$(ACCOUNT)/id))
	@scripts/fetch.py $(ACCOUNT) $(ID) >archive/$(ACCOUNT)/tmp
	@make append ACCOUNT=$(ACCOUNT)

append:
	@sed -i '' 's!\http\(s\)\{0,1\}://[^[:space:]]*!!g' archive/$(ACCOUNT)/tmp
	@head -n 1 archive/$(ACCOUNT)/tmp > archive/$(ACCOUNT)/id
	@tail -n +2 archive/$(ACCOUNT)/tmp >> archive/$(ACCOUNT)/log
	@awk '!x[$$0]++' <archive/$(ACCOUNT)/log >archive/$(ACCOUNT)/tmp
	@sed '/^$$/d' <archive/$(ACCOUNT)/tmp >archive/$(ACCOUNT)/log
	@rm archive/$(ACCOUNT)/tmp
	@scripts/parse.py $(ACCOUNT)

generate:
	@scripts/generate.py $(ACCOUNT)

parse:
	@scripts/parse.py $(ACCOUNT)

tweet:
	@make generate ACCOUNT=$(ACCOUNT) | scripts/tweet.py
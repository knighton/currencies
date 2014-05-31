three sources of currency conversions data, each with issues.

  A  daily_ecb         34 currencies   updated daily  unrestricted access

  B  xe_usd            80 currencies   live           crawling is banned

  C  fxstreet_usd      - over 130      live           - horrible ui
                       - guess 150ish                 - some of the data is *missing*
                                                      - you select subgroups of data
                                                        using POST

  D  exchangerate_usd  281 currencies  updated daily  don't redistribute

to be clear, i'm not trying to write an *accurate* currency converter.  i am
just trying to solve this problem well enough that i won't have to come back and
fuck around with it again for a long time.

usage:

  ./get.sh

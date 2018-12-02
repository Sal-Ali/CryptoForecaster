#load model from bin or model to use for decisions

#use predict of incoming feature to give out a recommendation

#act on recommendation then pass that action to database


# THEN implement backtester, and refitter
    # back-tester essentially evaluates the db data, flips
    # buy into sell if it was wrong, wrong determined by the
    # next result, last result changed to buy.
    # Takes old model data, refits this new data, does cv test to 
    # get the latest and greatest result and then saves that model 
    # into model slot
    
# FINALLY create driver to tie it all together, multithread (?)


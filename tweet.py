import tweepy

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main(compose):
    cfg = {
        "consumer_key"          : "X7qJ71E3WjBZypUSOsqs2ITTf",
        "consumer_secret"       : "PovSLMkdpvUUHdTuwNvPhoLWlvXME8NIzkESBeuNoTl64BVkjU",
        "access_token"          : "771072247385710592-2gdWUsJ5BT6V9gfDOPz4AmPEENpGWvu",
        "access_token_secret"   : "zGgLKKPvzBxfdeTMcIAj46g2132pXZWiygUhhlmZuJ0uP"
    }

    api = get_api(cfg)
    tweet = compose
    status = api.update_status(status=tweet)

if __name__ == "__main__":
  main()
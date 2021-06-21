import unittest
from src import util


class UtilTestCase(unittest.TestCase):
    """ Test cases for Util method """

    def test_referenced_tweet(self):
        ent = {'hashtags': ['Eurovision'], 'urls': ['https://t.co/4KvvbmfvUV'], 'mentions': ['veyselkarane']}
        result = {'_id': '1402305464625422342',
                  'raw_text': 'Kul, karşılık için esma çekmeyi çoğalttığı halde; esmayı çekmek bitmediği gibi, beklentiler '
                              'bitiyor ama sonuç değişmiyor. Yıllarca Müslümanları, sizleri Allah’a yaklaştırıyoruz diye '
                              'diye, gözümüzün içine baka baka Allah’tan uzaklaştırdılar. Kandırdılar!\n#Eurovision '
                              'Altınordu https://t.co/4KvvbmfvUV', 'author_id': '1402304961615179784',
                  'author_name': 'Aysıla Ünal', 'author_username': 'Ayslanal1',
                  'created_at': '2021-06-08T16:44:10.000Z',
                  'referenced_tweets': [{'id': '1396194560171290626', 'type': 'retweeted'}],
                  'complete_text': True, 'twitter_entities': ent, 'twitter_context_annotations': [
                {
                    'domain': {
                        'id': '118',
                        'name': 'Award Show',
                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                    'entity': {
                        'id': '1376864097594011648',
                        'name': 'Eurovision 2021'}},
                {
                    'domain': {
                        'id': '118',
                        'name': 'Award Show',
                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                    'entity': {
                        'id': '1376864097594011648',
                        'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 318, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'processed': False
                  }
        tweet = {
            'text': 'RT @veyselkarane: Kul, karşılık için esma çekmeyi çoğalttığı halde; esmayı çekmek '
                    'bitmediği gibi, beklentiler bitiyor ama sonuç değişmiyor.…',
            'author_id': '1402304961615179784', 'created_at': '2021-06-08T16:44:10.000Z',
            'id': '1402305464625422342',
            'public_metrics': {'retweet_count': 318, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
            'referenced_tweets': [{'type': 'retweeted', 'id': '1396194560171290626'}],
            'entities': {'mentions': [{'start': 3, 'end': 16, 'username': 'veyselkarane'}]}}
        includes = dict(users=[
            {'id': '744999730980098048', 'name': 'ℒ𝒶 𝓇𝒶𝑔𝒶𝓏𝓏𝒶 𝒹𝒾 𝒻𝓊𝑜𝒸𝑜', 'username': 'ele_masioli'},
            {'id': '1402304961615179784', 'name': 'Aysıla Ünal', 'username': 'Ayslanal1'},
            {'id': '1172195160802942976', 'name': 'лиза устала от долбоёбов, стэньте томаса раджи🐍',
             'username': 'viwqytvmer'},
            {'id': '1355882415668002822', 'name': '|Mary loves Cesare💜🏳\u200d🌈|Ceo of Screen di Cesi✨|',
             'username': 'vojdcesaree'}, {'id': '789519956086026240', 'name': 'ℳ☾', 'username': 'bizzledabs'},
            {'id': '1298333000493662209', 'name': 'Mary Knight', 'username': 'MaryKni40558994'},
            {'id': '1400168670966562816', 'name': 'ʕ⁎̯͡⁎ʔ༄', 'username': 'frogggk'},
            {'id': '1027265582532624385', 'name': 'Elizabeth', 'username': 'ThiIsYohan'},
            {'id': '1094580794453041152', 'name': '𝖇𝖊𝖗𝖎𝖑', 'username': 'berylova'},
            {'id': '40698893', 'name': 'sandra', 'username': 'pisceshtml'},
            {'id': '570712896', 'name': 'j⭕⭕st', 'username': 'JoostVanWell'},
            {'id': '470380963', 'name': 'Becky', 'username': 'Beclloyd99'},
            {'id': '1401703270775672835', 'name': 'thomas raggi dancing to 📻', 'username': 'raggisdance'},
            {'id': '485023886', 'name': 'marina velasco', 'username': 'velascomarina'},
            {'id': '1350886301885722626', 'name': 'riceball🧈', 'username': 'lTZAAAY'},
            {'id': '1154001109394087936', 'name': 'Letyy', 'username': 'Lety_2212'},
            {'id': '1513207362', 'name': '𝖘𝖎𝖈 𝖒𝖚𝖓𝖉𝖚𝖘 𝖈𝖗𝖊𝖆𝖙𝖚𝖘 𝖊𝖘𝖙', 'username': 'oh_mybrien'},
            {'id': '1316440976047706114', 'name': 'Monsterfucker Jhama Slutamil', 'username': 'monsterspriest2'},
            {'id': '118037355', 'name': 'PAT ∿', 'username': 'atleastimalive'},
            {'id': '1105946120637812737', 'name': '𝐝𝐚𝐯𝐢𝐝 🌧🏳️\u200d🌈', 'username': 'davidx_rs'}], tweets=[{
            'text': 'Io quando alla maturità mi diranno:"Abbiamo finito, puoi andare"...\n#maturita2021 #Eurovision '
                    '#maneskin https://t.co/sVgJWEYoe1',
            'author_id': '1102179926998958080',
            'entities': {
                'urls': [
                    {
                        'start': 104,
                        'end': 127,
                        'url': 'https://t.co/sVgJWEYoe1',
                        'expanded_url': 'https://twitter.com/EleonoraVannuc1/status/1400487925146689541/photo/1',
                        'display_url': 'pic.twitter.com/sVgJWEYoe1'}],
                'hashtags': [
                    {
                        'start': 68,
                        'end': 81,
                        'tag': 'maturita2021'},
                    {
                        'start': 82,
                        'end': 93,
                        'tag': 'Eurovision'},
                    {
                        'start': 94,
                        'end': 103,
                        'tag': 'maneskin'}]},
            'created_at': '2021-06-03T16:21:55.000Z',
            'context_annotations': [
                {
                    'domain': {
                        'id': '118',
                        'name': 'Award Show',
                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                    'entity': {
                        'id': '1376864097594011648',
                        'name': 'Eurovision 2021'}}],
            'id': '1400487925146689541',
            'public_metrics': {
                'retweet_count': 45,
                'reply_count': 4,
                'like_count': 359,
                'quote_count': 1}},
            {
                'text': 'Kul, karşılık için esma çekmeyi çoğalttığı halde; esmayı çekmek bitmediği gibi, beklentiler '
                        'bitiyor ama sonuç değişmiyor. Yıllarca Müslümanları, sizleri Allah’a yaklaştırıyoruz diye '
                        'diye, gözümüzün içine baka baka Allah’tan uzaklaştırdılar. Kandırdılar!\n#Eurovision '
                        'Altınordu https://t.co/4KvvbmfvUV',
                'author_id': '903172178128097281',
                'entities': {
                    'urls': [
                        {
                            'start': 276,
                            'end': 299,
                            'url': 'https://t.co/4KvvbmfvUV',
                            'expanded_url': 'https://twitter.com/veyselkarane/status/1396194560171290626/photo/1',
                            'display_url': 'pic.twitter.com/4KvvbmfvUV'}],
                    'hashtags': [
                        {
                            'start': 254,
                            'end': 265,
                            'tag': 'Eurovision'}]},
                'created_at': '2021-05-22T20:01:37.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}},
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1396194560171290626',
                'public_metrics': {
                    'retweet_count': 318,
                    'reply_count': 139,
                    'like_count': 522,
                    'quote_count': 4}},
            {
                'text': 'Thomas dancing to Jaja Ding Dong from Netflix’s Eurovision Song Contest: The Story of Fire '
                        'Saga🕺🏾 https://t.co/JThYqHMNq9',
                'author_id': '1401703270775672835',
                'entities': {
                    'urls': [
                        {
                            'start': 98,
                            'end': 121,
                            'url': 'https://t.co/JThYqHMNq9',
                            'expanded_url': 'https://twitter.com/raggisdance/status/1402304904291667968/video/1',
                            'display_url': 'pic.twitter.com/JThYqHMNq9'}],
                    'annotations': [
                        {
                            'start': 0,
                            'end': 5,
                            'probability': 0.7585,
                            'type': 'Person',
                            'normalized_text': 'Thomas'},
                        {
                            'start': 18,
                            'end': 31,
                            'probability': 0.3058,
                            'type': 'Other',
                            'normalized_text': 'Jaja Ding Dong'},
                        {
                            'start': 38,
                            'end': 44,
                            'probability': 0.5118,
                            'type': 'Organization',
                            'normalized_text': 'Netflix'}]},
                'created_at': '2021-06-08T16:41:57.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '86',
                            'name': 'Movie',
                            'description': 'A film like Rogue One: A Star Wars Story'},
                        'entity': {
                            'id': '1276128137080799233',
                            'name': 'Eurovision Song Contest: The Story of Fire Saga',
                            'description': 'Releases on June 26, 2020. (Netflix)'}},
                    {
                        'domain': {
                            'id': '87',
                            'name': 'Movie Genre',
                            'description': 'A movie genre like Action'},
                        'entity': {
                            'id': '856976685916237824',
                            'name': 'Comedy films',
                            'description': 'Comedy'}},
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}},
                    {
                        'domain': {
                            'id': '45',
                            'name': 'Brand Vertical',
                            'description': 'Top level entities that describe a Brands industry'},
                        'entity': {
                            'id': '781974597310615553',
                            'name': 'Entertainment'}},
                    {
                        'domain': {
                            'id': '46',
                            'name': 'Brand Category',
                            'description': 'Categories within Brand Verticals that narrow down the scope of Brands'},
                        'entity': {
                            'id': '781974597105094656',
                            'name': 'TV/Movies Related'}},
                    {
                        'domain': {
                            'id': '47',
                            'name': 'Brand',
                            'description': 'Brands and Companies'},
                        'entity': {
                            'id': '10026367762',
                            'name': 'Netflix'}}],
                'id': '1402304904291667968',
                'public_metrics': {
                    'retweet_count': 1,
                    'reply_count': 1,
                    'like_count': 6,
                    'quote_count': 3}},
            {
                'text': 'Che senso ha paragonare dei reality show all’eurovision ???? https://t.co/8QwgUlgtuH',
                'author_id': '1043237591297024001',
                'entities': {
                    'urls': [
                        {
                            'start': 61,
                            'end': 84,
                            'url': 'https://t.co/8QwgUlgtuH',
                            'expanded_url': 'https://twitter.com/carpediem_who/status/1402046529616158723',
                            'display_url': 'twitter.com/carpediem_who/…'}]},
                'created_at': '2021-06-08T10:32:32.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402211939669975041',
                'public_metrics': {
                    'retweet_count': 11,
                    'reply_count': 2,
                    'like_count': 252,
                    'quote_count': 0}},
            {
                'text': 'Primero: no idolatramos a Damiano, idolatramos a Måneskin\nSegundo: no nos gustan por el '
                        'simple hecho de que se maquillen, eso nos la suda lol, lo que nos gusta es su música '
                        '\nTercero: yo sí que no estoy haciendo absolutamente nada, ellos han ganado Eurovisión con '
                        'mi edad señora https://t.co/8VrOHrZXFZ',
                'author_id': '953011519436050432',
                'entities': {
                    'urls': [
                        {
                            'start': 278,
                            'end': 301,
                            'url': 'https://t.co/8VrOHrZXFZ',
                            'expanded_url': 'https://twitter.com/zorradeblanca/status/1401913690153177089',
                            'display_url': 'twitter.com/zorradeblanca/…'}],
                    'annotations': [
                        {
                            'start': 26,
                            'end': 32,
                            'probability': 0.9093,
                            'type': 'Person',
                            'normalized_text': 'Damiano'},
                        {
                            'start': 49,
                            'end': 56,
                            'probability': 0.8462,
                            'type': 'Person',
                            'normalized_text': 'Måneskin'}]},
                'created_at': '2021-06-08T12:12:52.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402237187035471879',
                'public_metrics': {
                    'retweet_count': 5,
                    'reply_count': 4,
                    'like_count': 25,
                    'quote_count': 1},
                'referenced_tweets': [
                    {
                        'type': 'quoted',
                        'id': '1401913690153177089'}]},
            {
                'text': '@Conor419 @MaryKni40558994 @DPJHodges @steviehcohen Also, 4 out of 5 Eurovision contests '
                        'were won under Labour!',
                'author_id': '81918911',
                'entities': {
                    'annotations': [
                        {
                            'start': 104,
                            'end': 109,
                            'probability': 0.6508,
                            'type': 'Organization',
                            'normalized_text': 'Labour'}],
                    'mentions': [
                        {
                            'start': 0,
                            'end': 9,
                            'username': 'Conor419'},
                        {
                            'start': 10,
                            'end': 26,
                            'username': 'MaryKni40558994'},
                        {
                            'start': 27,
                            'end': 37,
                            'username': 'DPJHodges'},
                        {
                            'start': 38,
                            'end': 51,
                            'username': 'steviehcohen'}]},
                'created_at': '2021-06-07T21:20:26.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402012598736936965',
                'public_metrics': {
                    'retweet_count': 0,
                    'reply_count': 1,
                    'like_count': 1,
                    'quote_count': 0},
                'referenced_tweets': [
                    {
                        'type': 'replied_to',
                        'id': '1401895149727367170'}]},
            {
                'text': '🕯 Carla for Eurovision 🕯\nhttps://t.co/PIx4apCexV',
                'author_id': '1314994577728831488',
                'entities': {
                    'urls': [
                        {
                            'start': 25,
                            'end': 48,
                            'url': 'https://t.co/PIx4apCexV',
                            'expanded_url': 'https://twitter.com/jescarchive/status/1198693119778336769/video/1',
                            'display_url': 'pic.twitter.com/PIx4apCexV'}],
                    'annotations': [
                        {
                            'start': 3,
                            'end': 7,
                            'probability': 0.6562,
                            'type': 'Person',
                            'normalized_text': 'Carla'}]},
                'created_at': '2021-06-08T13:26:25.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402255696033316871',
                'public_metrics': {
                    'retweet_count': 1,
                    'reply_count': 1,
                    'like_count': 18,
                    'quote_count': 1}},
            {
                'text': '@berylova @Eurovisn_Turkey Anlatmaya calistigin seyi anlatamamissin???',
                'author_id': '1162769754928685057',
                'created_at': '2021-06-08T16:36:40.000Z',
                'id': '1402303577041870854',
                'public_metrics': {
                    'retweet_count': 0,
                    'reply_count': 1,
                    'like_count': 0,
                    'quote_count': 0},
                'referenced_tweets': [
                    {
                        'type': 'replied_to',
                        'id': '1402299979960553487'}],
                'entities': {
                    'mentions': [
                        {
                            'start': 0,
                            'end': 9,
                            'username': 'berylova'},
                        {
                            'start': 10,
                            'end': 26,
                            'username': 'Eurovisn_Turkey'}]}},
            {
                'text': '🙏 "The courage to be oneself."\n\n🌈 #Eurovision winners @thisismaneskin are the cover '
                        'stars of @VanityFairIt\'s special Pride issue.\n \n✍️ — @willyleeadams '
                        '\n\nhttps://t.co/HZf9Uadamm',
                'author_id': '17198692',
                'entities': {
                    'urls': [
                        {
                            'start': 154,
                            'end': 177,
                            'url': 'https://t.co/HZf9Uadamm',
                            'expanded_url': 'https://wiwibloggs.com/2021/06/08/the-courage-to-be-oneself-maneskin'
                                            '-land-on-cover-of-vanity-fair-italias-special-pride-issue/265687/',
                            'display_url': 'wiwibloggs.com/2021/06/08/the…',
                            'images': [
                                {
                                    'url': 'https://pbs.twimg.com/news_img/1402289458419060744/mi4WyfNM?format=jpg'
                                           '&name=orig',
                                    'width': 800,
                                    'height': 600},
                                dict(
                                    url='https://pbs.twimg.com/news_img/1402289458419060744/mi4WyfNM?format=jpg&name'
                                        '=150x150',
                                    width=150, height=150)],
                            'status': 200,
                            'title': "Måneskin land on cover of Vanity Fair Italia's special Pride issue",
                            'description': "They're embracing tolerance and celebrating diversity. Now Måneskin have "
                                           "landed on Vanity Fair Italia's Pride issue!",
                            'unwound_url': 'https://wiwibloggs.com/2021/06/08/the-courage-to-be-oneself-maneskin-land'
                                           '-on-cover-of-vanity-fair-italias-special-pride-issue/265687/'}],
                    'hashtags': [
                        {
                            'start': 34,
                            'end': 45,
                            'tag': 'Eurovision'}],
                    'mentions': [
                        {
                            'start': 54,
                            'end': 69,
                            'username': 'thisismaneskin'},
                        {
                            'start': 93,
                            'end': 106,
                            'username': 'VanityFairIt'},
                        {
                            'start': 137,
                            'end': 151,
                            'username': 'willyleeadams'}]},
                'created_at': '2021-06-08T15:40:34.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402289457966026752',
                'public_metrics': {
                    'retweet_count': 28,
                    'reply_count': 0,
                    'like_count': 105,
                    'quote_count': 1}},
            {
                'text': 'Have to give a speech about Brexit this evening. In German. Bit of a shock! 🤯 Not public '
                        'though, sorry... or possibly for the best!\n\nIt\'s a bit of a struggle to explain the "but '
                        'why are they doing *that* to their economy?" sort of question that\'s inevitably going to '
                        'come...',
                'author_id': '17442320',
                'entities': {
                    'annotations': [
                        {
                            'start': 28,
                            'end': 33,
                            'probability': 0.6887,
                            'type': 'Other',
                            'normalized_text': 'Brexit'}]},
                'created_at': '2021-06-08T16:31:15.000Z',
                'id': '1402302213565947907',
                'public_metrics': {
                    'retweet_count': 5,
                    'reply_count': 27,
                    'like_count': 76,
                    'quote_count': 2}},
            {
                'text': 'Con la pérdida de las colonias surge el nacionalista español nostálgico incapaz de asimilar '
                        'que no importa a nadie, ni siquiera en Eurovisión. Se conforma entonces con disfrazar a '
                        'cabras y lanzar a paracaidistas contra farolas para olvidar el año 1898. 😂 '
                        'https://t.co/wzhTlDi9Qg https://t.co/JN4VV6xuwB',
                'author_id': '231221571',
                'entities': {
                    'urls': [
                        {
                            'start': 255,
                            'end': 278,
                            'url': 'https://t.co/wzhTlDi9Qg',
                            'expanded_url': 'https://twitter.com/blogsocietat/status/1402294149936713733/photo/1',
                            'display_url': 'pic.twitter.com/wzhTlDi9Qg'},
                        {
                            'start': 255,
                            'end': 278,
                            'url': 'https://t.co/wzhTlDi9Qg',
                            'expanded_url': 'https://twitter.com/blogsocietat/status/1402294149936713733/photo/1',
                            'display_url': 'pic.twitter.com/wzhTlDi9Qg'},
                        {
                            'start': 279,
                            'end': 302,
                            'url': 'https://t.co/JN4VV6xuwB',
                            'expanded_url': 'https://twitter.com/jwm_twittor/status/1402128252739588096',
                            'display_url': 'twitter.com/jwm_twittor/st…'}],
                    'annotations': [
                        {
                            'start': 131,
                            'end': 140,
                            'probability': 0.8071,
                            'type': 'Place',
                            'normalized_text': 'Eurovisión'}]},
                'created_at': '2021-06-08T15:59:13.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402294149936713733',
                'public_metrics': {
                    'retweet_count': 4,
                    'reply_count': 3,
                    'like_count': 12,
                    'quote_count': 0},
                'referenced_tweets': [
                    dict(type='quoted', id='1402128252739588096')]},
            {
                'text': '@thisismaneskin for @VanityFairIt ✨\nChe abbia inizio la #pridecatwalkchallenge.\nI Måneskin '
                        'si presentano, in occasione del Pride Month, più veri e liberi che mai. 🏳️\u200d🌈 '
                        'https://t.co/1Fzi2edit3',
                'author_id': '940864885528977408',
                'entities': {
                    'urls': [
                        {
                            'start': 168,
                            'end': 191,
                            'url': 'https://t.co/1Fzi2edit3',
                            'expanded_url': 'https://twitter.com/ManeskinFanClub/status/1402285763782455297/video/1',
                            'display_url': 'pic.twitter.com/1Fzi2edit3'}],
                    'hashtags': [
                        {
                            'start': 56,
                            'end': 78,
                            'tag': 'pridecatwalkchallenge'}],
                    'mentions': [
                        {
                            'start': 0,
                            'end': 15,
                            'username': 'thisismaneskin'},
                        {
                            'start': 20,
                            'end': 33,
                            'username': 'VanityFairIt'}]},
                'created_at': '2021-06-08T15:25:53.000Z',
                'id': '1402285763782455297',
                'public_metrics': {
                    'retweet_count': 109,
                    'reply_count': 2,
                    'like_count': 393,
                    'quote_count': 86}},
            {
                'text': 'quote and answer (blind channel fandom edition) #JoinTheDarkSide #Eurovision',
                'author_id': '1513207362',
                'created_at': '2021-05-21T11:43:08.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}},
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'entities': {
                    'hashtags': [
                        {
                            'start': 48,
                            'end': 64,
                            'tag': 'JoinTheDarkSide'},
                        {
                            'start': 65,
                            'end': 76,
                            'tag': 'Eurovision'}]},
                'id': '1395706724313612289',
                'public_metrics': {
                    'retweet_count': 1,
                    'reply_count': 2,
                    'like_count': 5,
                    'quote_count': 3}},
            {
                'text': '@monsterspriest2 ashjkshjkshajskj pensei em mata hari, nao tem nada a ver com a descrição '
                        'que tu deu, mas vou deixar aqui pq eu gostei da murga\n\nE AIII SIMM TIX AMORZINHO 💙 ÓBVIO '
                        'que Maneskin = tudo pra mim, mas TIX e Blind Channel são meus favs '
                        'também\nhttps://t.co/vmw4xw8Hqh',
                'author_id': '14277934',
                'entities': {
                    'urls': [
                        {
                            'start': 253,
                            'end': 276,
                            'url': 'https://t.co/vmw4xw8Hqh',
                            'expanded_url': 'https://www.youtube.com/watch?v=5ZVC6f9cXKk',
                            'display_url': 'youtube.com/watch?v=5ZVC6f…',
                            'images': [
                                {
                                    'url': 'https://pbs.twimg.com/news_img/1400053633568411648/H2qgkngx?format=jpg'
                                           '&name=orig',
                                    'width': 1280,
                                    'height': 720},
                                {
                                    'url': 'https://pbs.twimg.com/news_img/1400053633568411648/H2qgkngx?format=jpg'
                                           '&name=150x150',
                                    'width': 150,
                                    'height': 150}],
                            'status': 200,
                            'title': 'Efendi - Mata Hari - LIVE - Azerbaijan 🇦🇿 - First Semi-Final - Eurovision 2021',
                            'description': 'Efendi represented Azerbaijan in the First Semi-Final of the Eurovision '
                                           'Song Contest 2021 with the song Mata Hari-The Eurovision Song Contest '
                                           'celebrates dive...',
                            'unwound_url': 'https://www.youtube.com/watch?v=5ZVC6f9cXKk'}],
                    'annotations': [
                        {
                            'start': 49,
                            'end': 52,
                            'probability': 0.5784,
                            'type': 'Person',
                            'normalized_text': 'hari'}],
                    'mentions': [
                        {
                            'start': 0,
                            'end': 16,
                            'username': 'monsterspriest2'}]},
                'created_at': '2021-06-08T16:37:32.000Z',
                'id': '1402303792981348356',
                'public_metrics': {
                    'retweet_count': 0,
                    'reply_count': 2,
                    'like_count': 1,
                    'quote_count': 0},
                'referenced_tweets': [
                    {
                        'type': 'replied_to',
                        'id': '1402301817057337347'}]},
            {
                'text': 'JUSTICE FOR ANGGUN! 🇫🇷🖤\n\n#EUROVISION https://t.co/ZVcOe4MWjO',
                'author_id': '1153648371044892672',
                'entities': {
                    'urls': [
                        {
                            'start': 37,
                            'end': 60,
                            'url': 'https://t.co/ZVcOe4MWjO',
                            'expanded_url': 'https://twitter.com/DarkGa2/status/1402285618340806660/video/1',
                            'display_url': 'pic.twitter.com/ZVcOe4MWjO'}],
                    'hashtags': [
                        {
                            'start': 25,
                            'end': 36,
                            'tag': 'EUROVISION'}]},
                'created_at': '2021-06-08T15:25:19.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1402285618340806660',
                'public_metrics': {
                    'retweet_count': 1,
                    'reply_count': 1,
                    'like_count': 3,
                    'quote_count': 1}},
            {
                'text': 'Ojalá RTVE hiciera un Eurojunior para la temporada de otoño con temazos así, si tanto decían '
                        'que iban a dar todos sus esfuerzos en Eurovisión esta es su mejor opción de empezar \n '
                        'https://t.co/uHrfXCxBQj',
                'author_id': '708372825371975680',
                'entities': {
                    'urls': [
                        {
                            'start': 179,
                            'end': 202,
                            'url': 'https://t.co/uHrfXCxBQj',
                            'expanded_url': 'https://twitter.com/teleaudiencias/status/1285962629509521410/video/1',
                            'display_url': 'pic.twitter.com/uHrfXCxBQj'}],
                    'annotations': [
                        {
                            'start': 6,
                            'end': 9,
                            'probability': 0.5046,
                            'type': 'Organization',
                            'normalized_text': 'RTVE'},
                        {
                            'start': 22,
                            'end': 31,
                            'probability': 0.4077,
                            'type': 'Person',
                            'normalized_text': 'Eurojunior'},
                        {
                            'start': 131,
                            'end': 140,
                            'probability': 0.846,
                            'type': 'Place',
                            'normalized_text': 'Eurovisión'}]},
                'created_at': '2021-06-07T17:39:28.000Z',
                'context_annotations': [
                    {
                        'domain': {
                            'id': '118',
                            'name': 'Award Show',
                            'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {
                            'id': '1376864097594011648',
                            'name': 'Eurovision 2021'}}],
                'id': '1401956989517938689',
                'public_metrics': {
                    'retweet_count': 19,
                    'reply_count': 2,
                    'like_count': 102,
                    'quote_count': 5}}])
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_no_retweeted(self):
        ent = {'hashtags': ['Eurovision'], 'annotation': [{'normalized_text': 'Toñi Prieto',
                                                           'probability': 0.9891,
                                                           'type': 'Person'},
                                                          {'normalized_text': 'Ana Maria',
                                                           'probability': 0.9963,
                                                           'type': 'Person'}]}

        result = {'_id': '1402586088523317249',
                  'raw_text': 'Mucha alegría veo con la salida de Toñi Prieto cuando Ana Maria también esta desde hace años en la delegación española de #Eurovision y siguieron los mismos resultados',
                  'author_id': '849837630',
                  'author_name': 'Fran', 'author_username': '_Fr_an_',
                  'created_at': '2021-06-09T11:19:16.000Z',
                  'twitter_entities': ent, 'twitter_context_annotations':
                      [{'domain': {'id': '118', 'name': 'Award Show',
                                   'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'processed': False
                  }
        tweet = {'entities': {'hashtags': [{'start': 122, 'end': 133, 'tag': 'Eurovision'}], 'annotations': [
            {'start': 35, 'end': 45, 'probability': 0.9891, 'type': 'Person', 'normalized_text': 'Toñi Prieto'},
            {'start': 54, 'end': 62, 'probability': 0.9963, 'type': 'Person', 'normalized_text': 'Ana Maria'}]},
                 'id': '1402586088523317249', 'author_id': '849837630', 'created_at': '2021-06-09T11:19:16.000Z',
                 'text': 'Mucha alegría veo con la salida de Toñi Prieto cuando Ana Maria también esta desde hace años en la delegación española de #Eurovision y siguieron los mismos resultados',
                 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                 'context_annotations': [{'domain': {'id': '118', 'name': 'Award Show',
                                                     'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                          'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}]}

        includes = {'users': [
            {'id': '1239166689402589185', 'name': '🌻Abba 🌾 🇮🇹🇺🇦🇫🇮🇳🇴🇮🇸', 'username': 'palitodejoly7'},
            {'id': '237785012', 'name': 'Jose Julio Aranaz', 'username': 'jjaranaz94'},
            {'id': '1386777042918772738', 'name': 'antena 🎸', 'username': 'shadwmosez'},
            {'id': '849837630', 'name': 'Fran', 'username': '_Fr_an_'}], 'tweets': [
            {'entities': {'mentions': [{'start': 0, 'end': 7, 'username': '_3nFin'}]}, 'id': '1402584852722032642',
             'author_id': '3078157767', 'created_at': '2021-06-09T11:14:22.000Z',
             'text': '@_3nFin idolatrado por llevar ropa alternativa y pintarse los ojos claro lo de que tiene un talentazo que flipas y que gano eurovision ya lo dejamos para otro dia',
             'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 1, 'quote_count': 0},
             'context_annotations': [{'domain': {'id': '118', 'name': 'Award Show',
                                                 'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                      'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}],
             'referenced_tweets': [{'type': 'replied_to', 'id': '1402583643483222016'}]}, {'entities': {
                'hashtags': [{'start': 1, 'end': 16, 'tag': 'FelizMiércoles'}, {'start': 19, 'end': 24, 'tag': 'Miki'},
                             {'start': 61, 'end': 68, 'tag': 'España'}, {'start': 87, 'end': 98, 'tag': 'Eurovisión'},
                             {'start': 102, 'end': 107, 'tag': 'Fran'}, {'start': 121, 'end': 126, 'tag': 'bote'}],
                'mentions': [{'start': 156, 'end': 170, 'username': 'pasapalabrat5'},
                             {'start': 174, 'end': 187, 'username': 'ChristianG_7'},
                             {'start': 217, 'end': 233, 'username': 'TrasElValle_OBC'}], 'urls': [
                    {'start': 253, 'end': 276, 'url': 'https://t.co/ZmYmUU2TVU',
                     'expanded_url': 'http://obamaschannel.blogspot.com/2019/01/entre-eurovision-y-pasapalabra.html?m=1',
                     'display_url': 'obamaschannel.blogspot.com/2019/01/entre-…', 'images': [
                        {'url': 'https://pbs.twimg.com/news_img/1400437443107725318/K89F4GTG?format=jpg&name=orig',
                         'width': 1200, 'height': 630},
                        {'url': 'https://pbs.twimg.com/news_img/1400437443107725318/K89F4GTG?format=jpg&name=150x150',
                         'width': 150, 'height': 150}], 'status': 200, 'title': 'Entre "Eurovisión" y "Pasapalabra"',
                     'description': 'Blog sobre Información y Entretenimiento. Noticias, Deportes, Cultura, Sociedad.',
                     'unwound_url': 'https://obamaschannel.blogspot.com/2019/01/entre-eurovision-y-pasapalabra.html?m=1'}]},
                'id': '1090494288461529088',
                'author_id': '237785012',
                'created_at': '2019-01-30T06:17:53.000Z',
                'text': '¡#FelizMiércoles'
                        '!\n\n#Miki se '
                        'convirtió en el '
                        'representante de '
                        '#España en el '
                        'festival de '
                        '#Eurovisión, '
                        'y #Fran consiguió '
                        'el #bote de 1 542 '
                        '000 "eurazos" en '
                        'el @PasapalabraT5 '
                        'de '
                        '@ChristianG_7.\n'
                        '\nTe lo contamos '
                        'todo, '
                        'en el '
                        '@TrasElValle_OBC, '
                        'a un solo '
                        'click:\n\nhttps'
                        '://t.co/ZmYmUU2TVU',
                'public_metrics': {
                    'retweet_count': 114,
                    'reply_count': 0,
                    'like_count': 3,
                    'quote_count': 0},
                'context_annotations': [{
                    'domain': {
                        'id': '3',
                        'name': 'TV Shows',
                        'description': 'Television shows from around the world'},
                    'entity': {
                        'id': '10028259473',
                        'name': 'Pasapalabra'}},
                    {
                        'domain': {
                            'id': '3',
                            'name': 'TV Shows',
                            'description': 'Television shows from around the world'},
                        'entity': {
                            'id': '10053505069',
                            'name': 'Eurovision 2018'}}]},
            {'id': '1402283526167404544', 'entities': {'annotations': [
                {'start': 0, 'end': 15, 'probability': 0.8965, 'type': 'Person', 'normalized_text': 'Rafał Brzozowski'},
                {'start': 79, 'end': 86, 'probability': 0.9239, 'type': 'Other', 'normalized_text': 'The Ride'},
                {'start': 110, 'end': 116, 'probability': 0.5974, 'type': 'Product', 'normalized_text': 'Twitter'}],
                'urls': [
                    {'start': 141, 'end': 164, 'url': 'https://t.co/ZHWL9taMkY',
                     'expanded_url': 'https://twitter.com/FakeEuroNews/status/1402283526167404544/photo/1',
                     'display_url': 'pic.twitter.com/ZHWL9taMkY'}]},
             'author_id': '1388924122198122497', 'created_at': '2021-06-08T15:17:00.000Z',
             'text': "Rafał Brzozowski is going to send out a free signed CD of his Eurovision song 'The Ride' to all "
                     "the people on Twitter who hate him the most. https://t.co/ZHWL9taMkY",
             'public_metrics': {'retweet_count': 5, 'reply_count': 0, 'like_count': 38, 'quote_count': 9},
             'context_annotations': [{'domain': {'id': '46', 'name': 'Brand Category',
                                                 'description': 'Categories within Brand Verticals that narrow down '
                                                                'the scope of Brands'},
                                      'entity': {'id': '781974596752842752', 'name': 'Services'}},
                                     {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'},
                                      'entity': {'id': '10045225402', 'name': 'Twitter'}}, {
                                         'domain': {'id': '118', 'name': 'Award Show',
                                                    'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                         'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}]}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_geo(self):
        ent = {'hashtags': ['Eurovision'], 'annotation': [{'normalized_text': 'TVE',
                                                           'probability': 0.847,
                                                           'type': 'Organization'},
                                                          {'normalized_text': 'Ana Bordas Toñi '
                                                                              'Prieto',
                                                           'probability': 0.8826,
                                                           'type': 'Person'},
                                                          {'normalized_text': 'RTVE',
                                                           'probability': 0.5524,
                                                           'type': 'Organization'}]}
        result = {'_id': '1402573825569603584',
                  'raw_text': 'Contar la verdad de que TVE  no seguirá haciendo autocrítica,malas elecciones,pésimas '
                              'puestas en escena,mala gestión ,cumplir los deseos del artista,elección de buena '
                              'canción en '
                              '#Eurovision .Ana Bordas Toñi Prieto son tal para cual .El presidente de RTVE no ha hecho nada . '
                              '😡😡',
                  'author_id': '1079696713609342981',
                  'author_name': 'Ricardo 🇮🇨', 'author_username': 'Ricardogalgomez',
                  'created_at': '2021-06-09T10:30:33.000Z',
                  'twitter_entities': ent, 'twitter_context_annotations':
                      [{'domain': {'id': '118', 'name': 'Award Show',
                                   'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                        'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}],
                  'geo': {'geo_id': 'a6a7a5f5b5f9a4c9', 'country': 'Spagna', 'city': 'Tegueste, España'},
                  'metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 1, 'quote_count': 0},
                  'processed': False
                  }

        tweet = {'author_id': '1079696713609342981', 'created_at': '2021-06-09T10:30:33.000Z',
                 'text': 'Contar la verdad de que TVE  no seguirá haciendo autocrítica,malas elecciones,pésimas '
                         'puestas en escena,mala gestión ,cumplir los deseos del artista,elección de buena canción en '
                         '#Eurovision .Ana Bordas Toñi Prieto son tal para cual .El presidente de RTVE no ha hecho nada . '
                         '😡😡',
                 'id': '1402573825569603584',
                 'entities': {'hashtags': [{'start': 178, 'end': 189, 'tag': 'Eurovision'}], 'annotations': [
                     {'start': 24, 'end': 26, 'probability': 0.847, 'type': 'Organization', 'normalized_text': 'TVE'},
                     {'start': 191, 'end': 212, 'probability': 0.8826, 'type': 'Person',
                      'normalized_text': 'Ana Bordas Toñi Prieto'},
                     {'start': 250, 'end': 253, 'probability': 0.5524, 'type': 'Organization',
                      'normalized_text': 'RTVE'}]}, 'geo': {'place_id': 'a6a7a5f5b5f9a4c9'},
                 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 1, 'quote_count': 0},
                 'context_annotations': [{'domain': {'id': '118', 'name': 'Award Show',
                                                     'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                          'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}]}

        includes = {'users': [{'id': '374420085', 'name': 'Doc Holiday #TeamZeroCovid 🧬🏝', 'username': 'doc53577'},
                              {'id': '547957320', 'name': 'Σελ · Mauz', 'username': 'mauzemontole'},
                              {'id': '239078270', 'name': '~BoniManu~', 'username': 'manueluchi'},
                              {'id': '1364151210266267652', 'name': 'val 🔗🎀🧊🌷', 'username': 'GOTXTINI'},
                              {'id': '2399437797', 'name': '🌸', 'username': 'CamilaItsMe'},
                              {'id': '2957968714', 'name': 'MissOlya', 'username': 'misssolyaa'},
                              {'id': '918625730958897154', 'name': 'Aarón B.', 'username': 'aaronbntz'},
                              {'id': '175387235', 'name': 'Alberto 🤡', 'username': 'AlbertoBfan'},
                              {'id': '255046581', 'name': '🎮Hector Zangetsu🎮 #TeamLoneliness🕶',
                               'username': 'HectorFer777'},
                              {'id': '490664492', 'name': 'RoRo', 'username': 'RoRoandGo'},
                              {'id': '1297594787860807680', 'name': 'Eurofanix', 'username': 'Eurofanix'},
                              {'id': '1088742039070613505', 'name': 'Alberto López Delgado🔻🏳️\u200d🌈',
                               'username': 'albertolode'},
                              {'id': '2719574635', 'name': 'fefe', 'username': 'fatouchibi'},
                              {'id': '1079696713609342981', 'name': 'Ricardo 🇮🇨', 'username': 'Ricardogalgomez'},
                              {'id': '1085084671', 'name': "I'm Only A Ren 🇩🇪✌🏾", 'username': 'eurenvision'},
                              {'id': '1371588271751434249', 'name': 'chiara', 'username': 'chiaraserra_'},
                              {'id': '1334530631649415169', 'name': 'Mike Crystal', 'username': 'MikeCrystal3'},
                              {'id': '1173192487176953857', 'name': 'Zak ❤️💚💙', 'username': 'Zaknair'},
                              {'id': '4202091699', 'name': 'Francy🌹🇮🇹', 'username': 'francy_1518'},
                              {'id': '171713658', 'name': 'Carlos', 'username': 'car_vlc'},
                              {'id': '1342411798125928449', 'name': 'cosmo ✩', 'username': 'lesbo4drm'},
                              {'id': '332157525', 'name': 'PEKAS', 'username': 'sergiopekas_'},
                              {'id': '1066439419396268032', 'name': 'KamiLo 🐯', 'username': 'mxriogxr'},
                              {'id': '1347345180010151936', 'name': 'måneskin 🇵🇸', 'username': 'hisokallumi'},
                              {'id': '35748752', 'name': 'sofokleous10-www.oikonomia.gr', 'username': 'sofokleous10'},
                              {'id': '3331278838', 'name': 'esma is an anti-romantic', 'username': 'esmatman'},
                              {'id': '802968876212428801', 'name': '🌺jess🌺', 'username': '__RedLily__'},
                              {'id': '1249680826192867329', 'name': 'The Real Mapacho', 'username': 'TMapacho'},
                              {'id': '1220731227356921859', 'name': 'ℰlayne ℰvans', 'username': 'missamxrican'},
                              {'id': '434062657', 'name': 'Ralph Jones', 'username': 'OhHiRalphJones'},
                              {'id': '832636450864668672', 'name': 'Måneskin España ™ 🇪🇸🟪🇮🇹',
                               'username': 'maneskin_esp'},
                              {'id': '1348632640476344320', 'name': 'oscarmorenonfire', 'username': 'tomamoreno'},
                              {'id': '1132270626419499010', 'name': 'lyss', 'username': 'tksfairy'},
                              {'id': '1039265437', 'name': 'Ghenadi Avricenco', 'username': 'Ghenadiav'},
                              {'id': '1358479324567994370', 'name': 'VAMPIRA_ASESINA', 'username': 'VampiraAsesina'},
                              {'id': '1260255814834630659', 'name': 'Chlo✨', 'username': 'chlooss'},
                              {'id': '894660967342256128', 'name': 'Jalp', 'username': 'Jalp__'},
                              {'id': '4009119861', 'name': '🌈Art UR', 'username': 'Daku_uwu'},
                              {'id': '98677620', 'name': 'ElDesmarque', 'username': 'eldesmarque'},
                              {'id': '966641732417925120', 'name': 'Gabriel CHOULET', 'username': 'GabrielChoulet'},
                              {'id': '1618636674', 'name': 'amargader', 'username': 'Amargader_90'},
                              {'id': '1284650617311502336', 'name': 'Jo', 'username': 'JoArilenaStan'},
                              {'id': '1271983795', 'name': 'Ŋefiu', 'username': 'JoNefiu'},
                              {'id': '1382350484485373957', 'name': 'Marlena', 'username': 'OCajOdNane'},
                              {'id': '735847830', 'name': 'Nerea 🇫🇮', 'username': 'itsnereayall'},
                              {'id': '521296695', 'name': 'nana; lividi sui gomiti', 'username': 'namelessn4na'},
                              {'id': '1228334637744873472', 'name': 'raulindignado', 'username': 'raulhago02'},
                              {'id': '1234116883084914690', 'name': 'Yorch 🌍✈️📺🇪🇸🍕🎹🤓😷🦁♐',
                               'username': 'Yorchff'},
                              {'id': '707261460574031873', 'name': 'Caos', 'username': 'mrcaos99'},
                              {'id': '175355774', 'name': '🇨🇵•𝒞𝒶𝓈𝓈𝒶𝓃𝒹𝓇𝒶 𓆟𓆜𓆞', 'username': 'Miisscassy'},
                              {'id': '909030260112592897', 'name': 'Orage de Merde', 'username': 'squierbassvi'},
                              {'id': '65077015', 'name': '🏳️\u200d🌈 Jota 🏳️\u200d🌈', 'username': 'lord_kenneth'},
                              {'id': '1206417376457048064', 'name': 'NME Australia', 'username': 'nmeaustralia'},
                              {'id': '1723676616', 'name': 'Aria🪐🍷|| liam owns my dear patience heart|habits',
                               'username': 'ila_lom'},
                              {'id': '1284557549723955200', 'name': 'Spinazzolaro💙🇮🇹', 'username': 'SpinaFan'},
                              {'id': '1230629606', 'name': 'ålkem', 'username': 'fucking_alone_'},
                              {'id': '1554264877', 'name': 'GorgoNico 🇪🇸', 'username': 'Gorgo_Nico'},
                              {'id': '57935555', 'name': 'mimi. | 🇮🇹 maneskin supremacy', 'username': 'miemzel'},
                              {'id': '1030390746132738048', 'name': 'Ana', 'username': 'anavilla_8'},
                              {'id': '1080939064277245952', 'name': 'ethan torchio’s bf (REAL)',
                               'username': 'silkylucifer'},
                              {'id': '1006635468967108609', 'name': 'Valta🌻', 'username': '_valta'},
                              {'id': '1392736200969048066', 'name': '✡︎ | einav ♡’ loki', 'username': 'ilymaneskin'},
                              {'id': '1267083808534417409', 'name': 'Luffy', 'username': 'P9prejgome'},
                              {'id': '1397985102852919296', 'name': 'emily✨🌙', 'username': 'xlovemaneskin'},
                              {'id': '486704605', 'name': 'Daniele San (ダニエレさん)', 'username': 'danny_luca'},
                              {'id': '111127337', 'name': 'Brendan A Jones', 'username': 'brandybongos'},
                              {'id': '918991953387237376', 'name': 'Mave', 'username': 'Cruelladevil29'},
                              {'id': '976231845590392832', 'name': 'valentina', 'username': 'valecreed'},
                              {'id': '1246966607760502786', 'name': 'den', 'username': 'icarvsroad'},
                              {'id': '1060926144021741568', 'name': 'heide', 'username': 'heeeeida'},
                              {'id': '598775097', 'name': 'Vicente Rico 🤐😇', 'username': 'YTanRicamente'},
                              {'id': '1334286777734098945', 'name': 'V | ia', 'username': 'T0KY0GURU'},
                              {'id': '1249688489383297025', 'name': 'ᒪᗩᑌᖇᗩ ʍσση', 'username': 'LauraMoon312'},
                              {'id': '1393002474', 'name': '\u200fً', 'username': 'freddiemyqueen'},
                              {'id': '255541842', 'name': 'Larry Francisco', 'username': 'perrocatalan'},
                              {'id': '1669989438', 'name': 'amandine ~ 🇮🇹', 'username': 'zittieangelis'},
                              {'id': '1394978680796033025', 'name': 'Kitty Folyen🦹\u200d♀️',
                               'username': 'Kittyfolyen_'},
                              {'id': '2281371873', 'name': 'toni.', 'username': 'jodidomugiwara'},
                              {'id': '2739407928', 'name': '𝗮𝗻𝗸𝗮 🦥', 'username': 'ahxyv'},
                              {'id': '1117517589264109568', 'name': 'BARBAS', 'username': 'estatodocupao'},
                              {'id': '3435678045', 'name': '⚡Niña Kamikaze⚡', 'username': 'KngdmOfParadox'},
                              {'id': '1384212905231454213', 'name': 'aaronprod', 'username': 'aaronprod1'},
                              {'id': '353076407', 'name': 'LukaES 🏳️\u200d🌈', 'username': 'LukaEurovision'},
                              {'id': '1402517735263723521', 'name': 'andji ♡', 'username': 'miomaneskin'},
                              {'id': '1037795687172321280', 'name': '𝚟𝚎𝚗𝚝’𝚊𝚗𝚗𝚒🌙✨𝙼å𝚗𝚎𝚜𝚔𝚒𝚗 𝟸𝟺/𝟽',
                               'username': 'absenceofcaos'},
                              {'id': '1346421597477986305', 'name': '🧬𝕣ꪖ𝕥ꪮꪀ🧬 🇦🇲', 'username': 'SanMarkand'},
                              {'id': '357484305', 'name': 'Bry 🤪', 'username': 'bryan_gomez_'},
                              {'id': '170068394', 'name': 'Eurovision-Spain.com | PrePartyES',
                               'username': 'eurospaincom'},
                              {'id': '2800562343', 'name': 'Still hopeless 🌈', 'username': 'Carmenchutu96'},
                              {'id': '1233053793387872256', 'name': 'Dante', 'username': 'monsgnrdnt'},
                              {'id': '1288957019697876997', 'name': 'mªr¡ª | was hwpayno', 'username': '96danglis'},
                              {'id': '4882635989', 'name': 'Juan Pablo Jimenez P', 'username': 'juanpajimper'},
                              {'id': '324547071', 'name': 'Irene Astorga', 'username': 'ireneastped'},
                              {'id': '1206289674500739077', 'name': '##ben ✨🌙 21 !!', 'username': 'pasimetelis'},
                              {'id': '1171604034', 'name': 'Elisabeth 🍀', 'username': 'elisabethmnv01'},
                              {'id': '4911172522', 'name': 'killer queen. ⵣ 💗💜💙', 'username': 'myaddictionhs'},
                              {'id': '1132220300161167360', 'name': 'Lisca🖤 loves måneskin :)',
                               'username': 'domscottoncandy'},
                              {'id': '1100079317898416128', 'name': 'Eurovision Stan🇬🇷🇷🇴🇨🇾🇦🇿🇸🇲',
                               'username': 'Eurofan_gh2'},
                              {'id': '773630316', 'name': '𝐦𝐢𝐜𝐡𝐞𝐥𝐚̊ 🌹', 'username': 'avdoremich'},
                              {'id': '3555655817', 'name': 'ً', 'username': 'escIipse'},
                              {'id': '940864885528977408', 'name': 'MOFC: MÅNESKIN OFFICIAL FANCLUB',
                               'username': 'ManeskinFanClub'},
                              {'id': '1268330194420596738', 'name': 'El Gatico Sobresalto ❤️💛💜',
                               'username': 'SalennSaberhage'},
                              {'id': '3039550246', 'name': '𝖋𝖎𝖓𝖆𝖑 𝖋𝖆𝖓𝖙𝖆𝖘𝖞 𝖑𝖔𝖛𝖊',
                               'username': 'xdanib99'},
                              {'id': '1388885407782350855', 'name': 'Globetrotting', 'username': 'GlobetrottngPMR'},
                              {'id': '1377043748366901256', 'name': '🥑 quo', 'username': 'VRDSFIRE'},
                              {'id': '129382723', 'name': 'Justice, Equality, and Rights',
                               'username': 'News_RightsTwit'},
                              {'id': '1178956601954160640', 'name': 'OlivieR', 'username': 'theotheroliver'},
                              {'id': '569268081', 'name': 'soy RARA... que pasa??', 'username': 'ferchu_finish'},
                              {'id': '2390971794', 'name': 'David', 'username': 'davidfesoria'},
                              {'id': '1242811321810325505', 'name': '𝐃𝐀𝐕𝐈𝐗 🥀', 'username': '_d_a_v_i_x_'},
                              {'id': '1087324795384020992', 'name': 'Katrin', 'username': 'mozzarella_2109'},
                              {'id': '1391436781749477378', 'name': 'Блядский цирк🤡', 'username': 'iQC389dRrsBgcuv'},
                              {'id': '917820416986701824', 'name': 'José Ruiz Molina', 'username': 'JosRuizMolina6'},
                              {'id': '325653066', 'name': 'Gemmα ♎ | #Italy22 🇮🇹', 'username': 'gemtavih'},
                              {'id': '1224832023891775493', 'name': 'Là-haut', 'username': 'lahautoficial'},
                              {'id': '2942538010', 'name': 'Maite', 'username': 'maiteelspins'},
                              {'id': '405077212', 'name': 'Borja 🇸🇪', 'username': 'BorjaVicioso'},
                              {'id': '1227547791444074496', 'name': 'lorenasainzmartinez',
                               'username': 'lorenasainzmar1'},
                              {'id': '9330602', 'name': 'BILD Promis', 'username': 'BILD_Promis'},
                              {'id': '1224465469261873155', 'name': 'Luis', 'username': 'luuis_t'},
                              {'id': '1074675306043080704', 'name': 'onlypain.com/bein', 'username': 'ughh_bein'},
                              {'id': '3401083019', 'name': 'noe²', 'username': 'ilmiorumore'},
                              {'id': '2181961613', 'name': 'mason', 'username': 'mason849'},
                              {'id': '84822972', 'name': 'Il Multipolarista', 'username': 'Desmondo90'},
                              {'id': '1270507003203461124', 'name': 'ᴹᵃᵈᵉˡᵉⁱⁿᵉ ᵈᵃⁱˡʸ ˢᵗʳᵘᵍᵍˡᵉˢ/beidou haver!!!/',
                               'username': 'zhonglithighs'},
                              {'id': '1224408806895116289', 'name': 'Fans Eurovision', 'username': 'FansEurovision1'},
                              {'id': '141776662', 'name': 'pepē', 'username': 'cruluke_pe'},
                              {'id': '35290181', 'name': 'Miguelloop⁴ 🪐', 'username': 'Mikelicious'},
                              {'id': '4227134441', 'name': 'RUMORE94', 'username': 'sergiorumo94'},
                              {'id': '927655767024525313', 'name': 'Anastasia', 'username': 'x_xana7'},
                              {'id': '1275368942115176450', 'name': 'FILLER QUEEN', 'username': 'FILLERQUEENPOD'},
                              {'id': '9330012', 'name': 'BILD News', 'username': 'BILD_News'},
                              {'id': '1260319415947735040', 'name': 'Carmen🌸', 'username': 'Carmen_RF7'},
                              {'id': '3062247261', 'name': 'Luis Fuster', 'username': 'luisfusteresc'},
                              {'id': '1150708716', 'name': 'Patricia', 'username': 'patrituits'},
                              {'id': '440833076', 'name': 'Jonathan Arrey', 'username': 'Jonathan_Arrey'},
                              {'id': '1183342512829849600', 'name': 'franci ⊬ hourly tata mic',
                               'username': 'hobifragolina'},
                              {'id': '15747827', 'name': 'Chris McCrudden', 'username': 'cmccrudden'},
                              {'id': '3157611431', 'name': 'tam', 'username': 'biteofmaneskin'},
                              {'id': '22696987', 'name': 'Flum', 'username': 'flumcake'},
                              {'id': '23352679', 'name': 'Natasha Duncan-Drake (call me Tasha, she/her)',
                               'username': 'beren_writes'},
                              {'id': '630083199', 'name': 'Antonio Martos ✈️💫', 'username': 'AntonioMartosR'},
                              {'id': '1003977581178380293', 'name': 'Lav🌿☽☾ is reading siege&storm|🌼 she / her',
                               'username': 'pr0ngsx'}, {'id': '427031058', 'name': 'V I K Y', 'username': 'viikygil'},
                              {'id': '154282704', 'name': 'Jorge', 'username': 'ChelistaDAmelin'},
                              {'id': '3040054968', 'name': '\u200eً', 'username': 'stvrmshine'},
                              {'id': '401019529', 'name': 'unCrazed', 'username': 'unCrazedUK'},
                              {'id': '1009910160221929474', 'name': 'p', 'username': 'paudiromeroo_'},
                              {'id': '1080961055101194240', 'name': 'ulia ᵕ̈', 'username': 'umhellox'},
                              {'id': '1251287863', 'name': 'Alexis Romero🏳️\u200d🌈', 'username': 'alexisromloz'},
                              {'id': '1857489698', 'name': 'Kyriakos Tsinivits 🇵🇹', 'username': 'KyriakoTsin'},
                              {'id': '60031601', 'name': 'Susanna Pucher', 'username': 'subflower'},
                              {'id': '949274546326163457', 'name': 'Rebe🎤', 'username': 'idolsxrebe'},
                              {'id': '730411824915611648', 'name': 'Jim 🙏 #UltraFanDeFlosMariae 🙏',
                               'username': 'JimJG7'},
                              {'id': '1239564187225010178', 'name': 'Cintia 🌌', 'username': 'lareira_a'},
                              {'id': '19620332', 'name': 'Mr Hits', 'username': 'darrenjl'},
                              {'id': '954112288897847296', 'name': 'Lynna🌹', 'username': 'Lynna218'},
                              {'id': '773542509200932864', 'name': 'Ani 🇧🇬', 'username': 'lauluka'},
                              {'id': '377657565', 'name': 'J. Villegas 🇪🇺', 'username': 'Juanvig4'},
                              {'id': '3506788397', 'name': 'Fernando G', 'username': 'fernan9595sport'},
                              {'id': '1345115621126778880', 'name': 'Victor (currently trying out she/they)',
                               'username': 'VictOWOr_'},
                              {'id': '2323072975', 'name': 'Rui Gonçalves / HATER DE TECLADO',
                               'username': 'ruisgoncalves'},
                              {'id': '341653029', 'name': 'Sara 🇮🇹 WE ARE THE WINNERS OF EUROVISION🇮🇹',
                               'username': '_SaraC_92'},
                              {'id': '1395055612174688258', 'name': 'Amsterdamse Taxi Service',
                               'username': 'AmsterdamseTaxi'},
                              {'id': '429945036', 'name': 'Dani Carpio', 'username': 'Dani_CarpioM'},
                              {'id': '73532530', 'name': '🏳️\u200d🌈 Chico Tóxico 🏳️\u200d🌈',
                               'username': 'ChicoToxico'},
                              {'id': '484781593', 'name': 'Kübra B ☮', 'username': 'decisionsmly'},
                              {'id': '2333795183', 'name': 'orléna 🌸', 'username': 'jsuisgemo'},
                              {'id': '146512211', 'name': 'EL_RUMBA_💙Oficial.', 'username': 'francisrumbamor'},
                              {'id': '374187801', 'name': 'TonyGG', 'username': 'TonyGG1991'},
                              {'id': '1316845909', 'name': 'Pol', 'username': 'PolMarin06'},
                              {'id': '61423662', 'name': '🎐', 'username': 'sti_boune'},
                              {'id': '236565801', 'name': 'Ger', 'username': 'Ger__86'},
                              {'id': '1168667694', 'name': '❄️Kai Barnes❄️ 🕹️ || ✪ WinterBaron enthusiast ✪',
                               'username': 'Karma_kai_'},
                              {'id': '1385867210908966914', 'name': 'Zo Bo', 'username': 'ZoBo_44'},
                              {'id': '41127025', 'name': '˙ɯ', 'username': 'miiglx'},
                              {'id': '198829810', 'name': 'El Periódico', 'username': 'elperiodico'},
                              {'id': '762693025571151872', 'name': 'Liam Slaughter', 'username': 's7aughter'},
                              {'id': '3527732955', 'name': 'Luigii', 'username': 'Itsxluigii'},
                              {'id': '1011362296910794752', 'name': 'ALBª 🌸', 'username': 'Albxsnch'},
                              {'id': '1386340096144670731', 'name': 'K', 'username': 'sukinamonoga_oi'},
                              {'id': '1016038581406609408', 'name': 'kimdongyul', 'username': 'kimdongyul9'},
                              {'id': '1335140918555533314', 'name': 'mrt_exit', 'username': 'mejorme_exit'},
                              {'id': '298037706', 'name': 'TOM', 'username': 'TOM_alfaromeo'},
                              {'id': '1349940787161796608', 'name': 'Mercedes Agnelli', 'username': 'mercedes101180'},
                              {'id': '701132700', 'name': '🇨🇾 🇸🇲🇷🇸/ LILY LANINI', 'username': 'Fuckmybodymind'},
                              {'id': '880352018', 'name': 'Antonio', 'username': 'AntonioJaani'},
                              {'id': '1291361901079822336', 'name': 'лу;;tw:рпп ψ🇮🇹', 'username': 'anxiouslou_'},
                              {'id': '1386359524500647937', 'name': 'Jungle Candle', 'username': 'junglecandle'},
                              {'id': '1004431455571861507', 'name': '✨Minerva✨', 'username': 'MinervadelRo1'},
                              {'id': '568747595', 'name': 'ale~º 🇮🇨x🏳️\u200d🌈 ✨ #HabráLeyTrans 🏳️\u200d⚧️ ✨',
                               'username': 'Aleph_Osho'}, {'id': '85969262', 'name': 'Abel ن', 'username': 'Abel1990'},
                              {'id': '360106945', 'name': 'Ricard Romero', 'username': 'ricard_romero'},
                              {'id': '1341510976760401920', 'name': 'Europeeeeee oooww', 'username': 'UnexpectedGay1'},
                              {'id': '367392152', 'name': '𝖃𝖆𝖇𝖎 𝕳', 'username': '_mynameisx'},
                              {'id': '1298738582589509634', 'name': 'STREAM LOCO LOCO 🌪', 'username': 'alvarovids'},
                              {'id': '803741842865090560', 'name': 'ESC_SPAIN 🇪🇸', 'username': 'EscSpain'},
                              {'id': '1914417937', 'name': '◇AiKa.ts', 'username': 'AiKa_25ts'},
                              {'id': '1389577317421355020', 'name': 'will eats concrete',
                               'username': 'concrete_eater_'},
                              {'id': '1044632521793785856', 'name': '€fan🌍', 'username': 'GorkusonR'},
                              {'id': '1278519498321125377', 'name': 'One Eurovision Winner', 'username': 'EurovisOne'},
                              {'id': '875003446725926912', 'name': 'Jose Manuel Diaz', 'username': 'josemadiaz2017'},
                              {'id': '408551247', 'name': 'mary jurjo', 'username': 'MaryJurjo'},
                              {'id': '178391413', 'name': 'RISKA!', 'username': 'amsterdannie'},
                              {'id': '1034849408444231681',
                               'name': '𝐵𝑒𝑎𝑡ℎ𝑦𝑟𝑎 / 🤍❤🤍 / 🇱🇹💖🏳️\u200d🌈 / ❤️🇸🇩', 'username': 'beathyra'},
                              {'id': '948580317446713349', 'name': 'Rob J', 'username': 'drashig199'},
                              {'id': '1413722209', 'name': 'RL', 'username': 'PlataformaRL'},
                              {'id': '996133951864561664', 'name': 'rα ☄', 'username': '1016wasabi'},
                              {'id': '337351696', 'name': 'Peter Bell', 'username': 'PeterBell7'},
                              {'id': '394315035', 'name': 'javi', 'username': 'Javi_Llavona'},
                              {'id': '2850997805', 'name': 'Fernando.', 'username': 'FerRMUCF_'},
                              {'id': '1263087916093444096', 'name': 'A', 'username': 'cxnstantinedark'},
                              {'id': '380392448', 'name': 'OM OptiMagazine', 'username': 'OptiMagazine'},
                              {'id': '1474554168', 'name': 'v.', 'username': 'victoria1442001'},
                              {'id': '390001653', 'name': 'Tressa', 'username': 'Tressa28'},
                              {'id': '2782632309', 'name': 'Eyner Fernández 🇪🇸', 'username': 'Eynerfdz'},
                              {'id': '799041096', 'name': 'Andreu del Camp', 'username': 'roigdelcamp'},
                              {'id': '803725716261060608', 'name': 'Apolo ➶ Me Quedo Tequila 🍾🧢',
                               'username': 'apolododici'},
                              {'id': '948672742760550400', 'name': 'Cesitah', 'username': 'asdf_cesar'},
                              {'id': '1262463304884269058', 'name': '🇷🇸Álvaro🌪🌪🌪', 'username': 'bemyguest2012'},
                              {'id': '605228639', 'name': 'Yupiii.gr', 'username': 'YupiiiGR'},
                              {'id': '2818153316', 'name': 'Due.', 'username': 'Dueylosabes'},
                              {'id': '746728833164914688', 'name': 'Neo ✨', 'username': 'kxrou7'},
                              {'id': '99369510', 'name': 'LeyLa.🥨⬡', 'username': 'LeyLaDona'},
                              {'id': '1050732729267093504', 'name': '*TRUMAN* 🏳️\u200d🌈 Chema',
                               'username': 'Papaia75'},
                              {'id': '1065981626302246912', 'name': 'ᴀᴋᴠᴀᴍᴀʀɪɴ @ ᴍɪᴋᴜ ᴇxᴘᴏ ᴏɴʟɪɴᴇ',
                               'username': 'akvamarin__'},
                              {'id': '1010639676405936128', 'name': 'Jabieh', 'username': 'riveraesconv'},
                              {'id': '1110060006857035782', 'name': 'gouu', 'username': 'ggooww7'},
                              {'id': '1534939958', 'name': 'Ume Matsuzaka, 24 años', 'username': 'vity_saxobeat'},
                              {'id': '2512820030', 'name': 'ALTERF', 'username': 'Alterf_8'},
                              {'id': '865294166', 'name': 'pau', 'username': 'pauvimee'},
                              {'id': '3028051851', 'name': 'Domenico 🦆', 'username': 'DToffolon'},
                              {'id': '1373179750739492864', 'name': '♡Black swan♡', 'username': 'i_black_swan'},
                              {'id': '1100468285055950849', 'name': 'Christina', 'username': 'XtinaXandra'},
                              {'id': '856878397', 'name': '🌊𝑴𝒂𝒓𝒊𝒆𝒏𝒇𝒍𝒂𝒕𝒆𝒏𝒕𝒂🌊 ❓🔇🎹',
                               'username': 'marienrosario'},
                              {'id': '1188560773158723585', 'name': 'Mcgm', 'username': 'Mcgm_99'},
                              {'id': '888369843459809280', 'name': 'Álvaro 🙌', 'username': 'alvaromart01'},
                              {'id': '1241090335826198529', 'name': 'marina💜', 'username': 'marinaguerre_'},
                              {'id': '1212288108927975424', 'name': 'Ava 🙃🇦🇺', 'username': 'vogelmeister22'},
                              {'id': '1006291042650542080', 'name': 'Five', 'username': 'cincoderegalo'},
                              {'id': '158415693', 'name': 'Sergio López 🏳️\u200d🌈🇪🇸', 'username': 'sergiolm216'},
                              {'id': '372730252', 'name': 'ålbarn osom', 'username': 'alba_awesome'},
                              {'id': '1131679892612026368', 'name': 'j', 'username': 'scret_grden'},
                              {'id': '1085119713129185283', 'name': 'mónica', 'username': '_monicamr'},
                              {'id': '12030152', 'name': 'soulfulsista', 'username': 'soulfulsista'},
                              {'id': '1254130795079499780', 'name': 'Alberto', 'username': 'SognoCarioca'},
                              {'id': '3668314036', 'name': 'm.', 'username': 'mimenteviajera'},
                              {'id': '1085902026003881984', 'name': 'Queer Longing', 'username': 'QueerLonging'},
                              {'id': '242703555', 'name': 'Terror in Planet🔻💚', 'username': 'terrorinplanet'},
                              {'id': '1257031414144544769', 'name': 'Miley', 'username': 'Ueeeueieue91911'}],
                    'tweets': [{'author_id': '753933431030120450',
                                'entities': {'mentions': [{'start': 0, 'end': 10, 'username': 'mxistente'}]},
                                'created_at': '2021-06-09T10:11:23.000Z',
                                'text': '@mxistente la jefa de la delegación española', 'id': '1402569002132643840',
                                'public_metrics': {'retweet_count': 0, 'reply_count': 1, 'like_count': 1,
                                                   'quote_count': 0},
                                'referenced_tweets': [{'type': 'replied_to', 'id': '1402566325482971137'}]},
                               {'author_id': '1197524826753249282', 'entities': {
                                   'mentions': [{'start': 0, 'end': 10, 'username': 'Nilsons92'},
                                                {'start': 11, 'end': 23, 'username': 'OriolSerra_'},
                                                {'start': 24, 'end': 35, 'username': 'futeliteut'},
                                                {'start': 36, 'end': 47, 'username': 'eldiarioes'}], 'annotations': [
                                       {'start': 78, 'end': 83, 'probability': 0.9008, 'type': 'Place',
                                        'normalized_text': 'España'},
                                       {'start': 86, 'end': 100, 'probability': 0.328, 'type': 'Other',
                                        'normalized_text': 'Eurovision 2021'}]},
                                'created_at': '2021-06-09T10:05:06.000Z',
                                'text': '@Nilsons92 @OriolSerra_ @futeliteut @eldiarioes Dios mío... Se refiere a '
                                        'solo España. Eurovision 2021 tuvo más de 183 millones de espectadores, superando a '
                                        'la anterior edición.',
                                'id': '1402567420468998146',
                                'public_metrics': {'retweet_count': 0, 'reply_count': 1, 'like_count': 0,
                                                   'quote_count': 0}, 'context_annotations': [
                                   {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'},
                                    'entity': {'id': '1145824682270007296', 'name': 'El Diario ',
                                               'description': 'spanish newspaper'}}, {
                                       'domain': {'id': '118', 'name': 'Award Show',
                                                  'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                       'entity': {'id': '1376864097594011648', 'name': 'Eurovision 2021'}}],
                                'referenced_tweets': [{'type': 'replied_to', 'id': '1402353929392906249'}]},
                               {'author_id': '1030390746132738048', 'created_at': '2021-06-09T09:55:43.000Z',
                                'text': 'Lo vuelvo a repetir. Ya no es solo por Eurovisión, es por el desastre que ha hecho Toñi con el entretenimiento de RTVE, que se ha basado en Cuéntame y en Masterchef hasta que ha quemado ambas.',
                                'id': '1402565062573924356',
                                'public_metrics': {'retweet_count': 2, 'reply_count': 2, 'like_count': 24,
                                                   'quote_count': 0}, 'context_annotations': [{'domain': {'id': '3',
                                                                                                          'name': 'TV Shows',
                                                                                                          'description': 'Television shows from around the world'},
                                                                                               'entity': {
                                                                                                   'id': '10029072721',
                                                                                                   'name': 'MasterChef',
                                                                                                   'description': 'The entertaining amateur cookery contest, where chefs attempt to create the most delicious dishes.'}},
                                                                                              {'domain': {'id': '118',
                                                                                                          'name': 'Award Show',
                                                                                                          'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                               'entity': {
                                                                                                   'id': '1376864097594011648',
                                                                                                   'name': 'Eurovision 2021'}}],
                                'entities': {'annotations': [
                                    {'start': 39, 'end': 48, 'probability': 0.5392, 'type': 'Place',
                                     'normalized_text': 'Eurovisión'},
                                    {'start': 83, 'end': 86, 'probability': 0.8017, 'type': 'Person',
                                     'normalized_text': 'Toñi'},
                                    {'start': 114, 'end': 117, 'probability': 0.4913, 'type': 'Place',
                                     'normalized_text': 'RTVE'},
                                    {'start': 154, 'end': 163, 'probability': 0.3305, 'type': 'Person',
                                     'normalized_text': 'Masterchef'}]}}, {'author_id': '110942823', 'entities': {
                            'mentions': [{'start': 0, 'end': 8, 'username': 'Vertele'}], 'urls': [
                                {'start': 248, 'end': 271, 'url': 'https://t.co/XwRHKSUjHz',
                                 'expanded_url': 'https://vertele.eldiario.es/1_7a5d32',
                                 'display_url': 'vertele.eldiario.es/1_7a5d32'}], 'annotations': [
                                {'start': 25, 'end': 28, 'probability': 0.5908, 'type': 'Organization',
                                 'normalized_text': 'RTVE'},
                                {'start': 39, 'end': 54, 'probability': 0.8537, 'type': 'Person',
                                 'normalized_text': 'Ana María Bordas'},
                                {'start': 75, 'end': 103, 'probability': 0.4399, 'type': 'Organization',
                                 'normalized_text': 'Entretenimiento y Divulgación'},
                                {'start': 119, 'end': 129, 'probability': 0.8771, 'type': 'Person',
                                 'normalized_text': 'Toñi Prieto'},
                                {'start': 136, 'end': 138, 'probability': 0.3778, 'type': 'Organization',
                                 'normalized_text': 'TVE'},
                                {'start': 235, 'end': 245, 'probability': 0.9277, 'type': 'Person',
                                 'normalized_text': 'Toñi Prieto'}]}, 'created_at': '2021-06-09T10:15:54.000Z',
                                                                           'text': '@Vertele Rectificación | RTVE '
                                                                                   'nombra a Ana María Bordas nueva directora '
                                                                                   'de Entretenimiento y Divulgación, '
                                                                                   'y mantiene a Toñi Prieto para '
                                                                                   'TVE.\n\nFuentes de la Corporación '
                                                                                   'explican a verTele la nueva estructura, '
                                                                                   'que no supone la salida de Toñi '
                                                                                   'Prieto:\nhttps://t.co/XwRHKSUjHz',
                                                                           'id': '1402570140189970435',
                                                                           'public_metrics': {'retweet_count': 5,
                                                                                              'reply_count': 0,
                                                                                              'like_count': 4,
                                                                                              'quote_count': 20},
                                                                           'referenced_tweets': [{'type': 'replied_to',
                                                                                                  'id': '1402562634935832580'}]},
                               {'author_id': '3028051851',
                                'entities': {'mentions': [{'start': 18, 'end': 28, 'username': 'mannegghj'}]},
                                'created_at': '2021-06-09T10:19:03.000Z',
                                'text': 'Riassunto di me e @mannegghj che ripetiamo insieme:\nPer fare il primo '
                                        'capitolo ci abbiamo messo quasi due ore, dopodiché pausa di 45 minuti '
                                        'guardando '
                                        'video di Lara Fabian, Cristian Imparato, Ti lascio una canzone e Patty Pravo che '
                                        'sbaglia il testo delle canzoni, poi 👇',
                                'id': '1402570932124803073',
                                'public_metrics': {'retweet_count': 0, 'reply_count': 1, 'like_count': 0,
                                                   'quote_count': 0}},
                               {'author_id': '948192116454449152', 'created_at': '2021-06-09T09:47:10.000Z',
                                'text': 'Blas no ganó Eurovision, pero consiguiendo el cese de Toñi se ha ganado el '
                                        'cariño de todo el público. https://t.co/rhPhRMd5rI',
                                'id': '1402562908828147717', 'entities': {'urls': [
                                   {'start': 102, 'end': 125, 'url': 'https://t.co/rhPhRMd5rI',
                                    'expanded_url': 'https://twitter.com/gossipkonigin/status/1402562908828147717'
                                                    '/photo/1',
                                    'display_url': 'pic.twitter.com/rhPhRMd5rI'}], 'annotations': [
                                   {'start': 0, 'end': 3, 'probability': 0.9769, 'type': 'Person',
                                    'normalized_text': 'Blas'},
                                   {'start': 13, 'end': 22, 'probability': 0.3626, 'type': 'Other',
                                    'normalized_text': 'Eurovision'},
                                   {'start': 54, 'end': 57, 'probability': 0.8612, 'type': 'Person',
                                    'normalized_text': 'Toñi'}]},
                                'public_metrics': {'retweet_count': 2, 'reply_count': 0, 'like_count': 5,
                                                   'quote_count': 0}, 'context_annotations': [{'domain': {'id': '118',
                                                                                                          'name': 'Award Show',
                                                                                                          'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                               'entity': {
                                                                                                   'id': '1376864097594011648',
                                                                                                   'name': 'Eurovision 2021'}}]},
                               {'author_id': '2366180366', 'created_at': '2021-05-25T09:41:41.000Z',
                                'text': 'I miss Eurovision', 'id': '1397125711887020032',
                                'public_metrics': {'retweet_count': 68, 'reply_count': 3, 'like_count': 449,
                                                   'quote_count': 5}, 'context_annotations': [{'domain': {'id': '118',
                                                                                                          'name': 'Award Show',
                                                                                                          'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                               'entity': {
                                                                                                   'id': '1376864097594011648',
                                                                                                   'name': 'Eurovision 2021'}}]},
                               {'author_id': '30538870', 'entities': {
                                   'mentions': [{'start': 0, 'end': 13, 'username': 'alba_awesome'},
                                                {'start': 14, 'end': 30, 'username': 'luismesacabello'},
                                                {'start': 31, 'end': 46, 'username': 'eurovision_tve'}]},
                                'created_at': '2021-06-09T10:01:20.000Z',
                                'text': '@alba_awesome @luismesacabello @eurovision_tve La has escuchado decir que '
                                        'quiere ir? No, pues ya está.',
                                'id': '1402566474531807233',
                                'public_metrics': {'retweet_count': 0, 'reply_count': 1, 'like_count': 0,
                                                   'quote_count': 0}, 'context_annotations': [{'domain': {'id': '118',
                                                                                                          'name': 'Award Show',
                                                                                                          'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                               'entity': {
                                                                                                   'id': '1376864097594011648',
                                                                                                   'name': 'Eurovision 2021'}}],
                                'referenced_tweets': [{'type': 'replied_to', 'id': '1402540062169088002'}]},
                               {'author_id': '846037320667217921', 'created_at': '2021-06-06T21:00:11.000Z',
                                'text': "Bottom at Eurovision. Bottom in G7 economic shock. Bottom in water quality. "
                                        "\n\nWhat happened to 'world-leading' Global Britain?\nhttps://t.co/PkhPvFlrW1",
                                'id': '1401645116947898368', 'entities': {'urls': [
                                   {'start': 127, 'end': 150, 'url': 'https://t.co/PkhPvFlrW1',
                                    'expanded_url': 'https://www.theguardian.com/environment/2021/jun/01/uk-ranked'
                                                    '-last-in-europe-for-bathing-water-quality-in-2020',
                                    'display_url': 'theguardian.com/environment/20…'}], 'annotations': [
                                   {'start': 10, 'end': 19, 'probability': 0.4175, 'type': 'Place',
                                    'normalized_text': 'Eurovision'},
                                   {'start': 118, 'end': 124, 'probability': 0.3955, 'type': 'Place',
                                    'normalized_text': 'Britain'}]},
                                'public_metrics': {'retweet_count': 384, 'reply_count': 76, 'like_count': 935,
                                                   'quote_count': 19}, 'context_annotations': [{'domain': {'id': '118',
                                                                                                           'name': 'Award Show',
                                                                                                           'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                                'entity': {
                                                                                                    'id': '1376864097594011648',
                                                                                                    'name': 'Eurovision 2021'}}]},
                               {'author_id': '307327967', 'created_at': '2021-06-08T16:38:13.000Z',
                                'text': 'La mayor sorpresa (para mal) de Eurovisión 2021. Lo visualizaba como el dark '
                                        'horse más claro de la edición y acabó siendo un pluf. Si es que Eurovisión es '
                                        'impredecible. https://t.co/GEwtRkaAzk',
                                'id': '1402303966168469507', 'entities': {'urls': [
                                   {'start': 169, 'end': 192, 'url': 'https://t.co/GEwtRkaAzk',
                                    'expanded_url': 'https://twitter.com/eurovisionario/status/1402189908811321353',
                                    'display_url': 'twitter.com/eurovisionario…'}], 'annotations': [
                                   {'start': 32, 'end': 46, 'probability': 0.4663, 'type': 'Other',
                                    'normalized_text': 'Eurovisión 2021'},
                                   {'start': 141, 'end': 150, 'probability': 0.5911, 'type': 'Place',
                                    'normalized_text': 'Eurovisión'}]},
                                'public_metrics': {'retweet_count': 4, 'reply_count': 2, 'like_count': 35,
                                                   'quote_count': 2}, 'context_annotations': [{'domain': {'id': '118',
                                                                                                          'name': 'Award Show',
                                                                                                          'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                               'entity': {
                                                                                                   'id': '1376864097594011648',
                                                                                                   'name': 'Eurovision 2021'}}],
                                'referenced_tweets': [{'type': 'quoted', 'id': '1402189908811321353'}]},
                               {'author_id': '443215710', 'entities': {
                                   'mentions': [{'start': 0, 'end': 15, 'username': 'terrorinplanet'},
                                                {'start': 16, 'end': 32, 'username': 'Vamosmalagacf__'},
                                                {'start': 33, 'end': 45, 'username': 'casasola_89'}]},
                                'created_at': '2021-06-09T10:14:22.000Z',
                                'text': '@terrorinplanet @Vamosmalagacf__ @casasola_89 En el Junior tenía más '
                                        'libertad si,y ahí se ha visto los resultados. Ojalá haga un buen trabajo',
                                'id': '1402569755349995522',
                                'public_metrics': {'retweet_count': 0, 'reply_count': 1, 'like_count': 0,
                                                   'quote_count': 0},
                                'referenced_tweets': [{'type': 'replied_to', 'id': '1402569464655364097'}]}],
                    'places': [{'name': 'Madrid', 'place_type': 'city', 'country_code': 'ES',
                                'geo': {'type': 'Feature', 'bbox': [-3.8890049, 40.3120713, -3.5180102, 40.6435181],
                                        'properties': {}}, 'id': '206c436ce43a43a3', 'country': 'Spagna',
                                'full_name': 'Madrid, España'},
                               {'name': 'Tegueste', 'place_type': 'city', 'country_code': 'ES',
                                'geo': {'type': 'Feature', 'bbox': [-16.3706565, 28.4901129, -16.291015, 28.5447471],
                                        'properties': {}}, 'id': 'a6a7a5f5b5f9a4c9', 'country': 'Spagna',
                                'full_name': 'Tegueste, España'},
                               {'name': 'Águilas', 'place_type': 'city', 'country_code': 'ES',
                                'geo': {'type': 'Feature', 'bbox': [-1.7053268, 37.3738142, -1.4684606, 37.5670171],
                                        'properties': {}}, 'id': '04cc65bb544b6409', 'country': 'Spagna',
                                'full_name': 'Águilas, España'},
                               {'name': 'Palma di Maiorca', 'place_type': 'city', 'country_code': 'ES',
                                'geo': {'type': 'Feature', 'bbox': [2.5637824, 39.1250696, 2.9761535, 39.6583262],
                                        'properties': {}}, 'id': '6c1be133511970bc', 'country': 'Spagna',
                                'full_name': 'Palma di Maiorca, Spagna'}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_mention(self):
        ent = {'hashtags': ['damikate', 'damianodavid', 'Eurovision'], 'mentions': ['marlenasslave'],
               'urls': ['https://t.co/wBDwmCgVjf', 'https://t.co/wBDwmCgVjf']}
        result = {'_id': '1402600531240046596',
                  'raw_text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate '
                              '#damianodavid #Eurovision https://t.co/wBDwmCgVjf',
                  'author_id': '957784397566050304',
                  'author_name': 'Milan ESC', 'author_username': 'milan_esc',
                  'created_at': '2021-06-09T12:16:40.000Z',
                  'referenced_tweets': [{'id': '1402600151789850626', 'type': 'retweeted'}],
                  'complete_text': True,
                  'twitter_entities': ent, 'twitter_context_annotations': [{'domain': {'id': '118',
                                                                                       'name': 'Award Show',
                                                                                       'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                            'entity': {'id': '1376864097594011648',
                                                                                       'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'processed': False
                  }
        tweet = {'created_at': '2021-06-09T12:16:40.000Z', 'entities': {
            'hashtags': [{'start': 84, 'end': 93, 'tag': 'damikate'}, {'start': 94, 'end': 107, 'tag': 'damianodavid'},
                         {'start': 108, 'end': 119, 'tag': 'Eurovision'}],
            'mentions': [{'start': 3, 'end': 17, 'username': 'marlenasslave'}]},
                 'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                 'id': '1402600531240046596', 'author_id': '957784397566050304', 'context_annotations': [{'domain': {
                'id': '118', 'name': 'Award Show', 'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                                          'entity': {
                                                                                                              'id': '1376864097594011648',
                                                                                                              'name': 'Eurovision 2021'}}],
                 'referenced_tweets': [{'type': 'retweeted', 'id': '1402600151789850626'}],
                 'text': 'RT @marlenasslave: [AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmC…'}
        includes = {'users': [{'id': '957784397566050304', 'name': 'Milan ESC', 'username': 'milan_esc'},
                              {'id': '1566112255', 'name': 'Miguel', 'username': 'teriz00'},
                              {'id': '1078462753461989378', 'name': 'juliå', 'username': 'athousandlivesz'}, ],
                    'tweets': [{'created_at': '2021-06-09T12:15:09.000Z', 'entities': {
                        'hashtags': [{'start': 65, 'end': 74, 'tag': 'damikate'},
                                     {'start': 75, 'end': 88, 'tag': 'damianodavid'},
                                     {'start': 89, 'end': 100, 'tag': 'Eurovision'}], 'urls': [
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'},
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'}]},
                                'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 1,
                                                   'quote_count': 0}, 'id': '1402600151789850626',
                                'author_id': '1400076690773135362', 'context_annotations': [{'domain': {'id': '118',
                                                                                                        'name': 'Award Show',
                                                                                                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                             'entity': {
                                                                                                 'id': '1376864097594011648',
                                                                                                 'name': 'Eurovision 2021'}}],
                                'text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmCgVjf'}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_mention2(self):
        ent = {'hashtags': ['damikate', 'damianodavid', 'Eurovision'], 'mentions': ['try', 'marlenasslave'],
               'urls': ['https://t.co/wBDwmCgVjf', 'https://t.co/wBDwmCgVjf']}
        result = {'_id': '1402600531240046596',
                  'raw_text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate '
                              '#damianodavid #Eurovision https://t.co/wBDwmCgVjf',
                  'author_id': '957784397566050304',
                  'author_name': 'Milan ESC', 'author_username': 'milan_esc',
                  'created_at': '2021-06-09T12:16:40.000Z',
                  'referenced_tweets': [{'id': '1402600151789850626', 'type': 'retweeted'}],
                  'complete_text': True,
                  'twitter_entities': ent, 'twitter_context_annotations': [{'domain': {'id': '118',
                                                                                       'name': 'Award Show',
                                                                                       'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                            'entity': {'id': '1376864097594011648',
                                                                                       'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'processed': False
                  }
        tweet = {'created_at': '2021-06-09T12:16:40.000Z', 'entities': {
            'hashtags': [{'start': 84, 'end': 93, 'tag': 'damikate'}, {'start': 94, 'end': 107, 'tag': 'damianodavid'},
                         {'start': 108, 'end': 119, 'tag': 'Eurovision'}],
            'mentions': [{'start': 3, 'end': 17, 'username': 'marlenasslave'}]},
                 'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                 'id': '1402600531240046596', 'author_id': '957784397566050304', 'context_annotations': [{'domain': {
                'id': '118', 'name': 'Award Show', 'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                                          'entity': {
                                                                                                              'id': '1376864097594011648',
                                                                                                              'name': 'Eurovision 2021'}}],
                 'referenced_tweets': [{'type': 'retweeted', 'id': '1402600151789850626'}],
                 'text': 'RT @marlenasslave: [AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmC…'}
        includes = {'users': [{'id': '957784397566050304', 'name': 'Milan ESC', 'username': 'milan_esc'},
                              {'id': '1566112255', 'name': 'Miguel', 'username': 'teriz00'},
                              {'id': '1078462753461989378', 'name': 'juliå', 'username': 'athousandlivesz'}, ],
                    'tweets': [{'created_at': '2021-06-09T12:15:09.000Z', 'entities': {
                        'hashtags': [{'start': 65, 'end': 74, 'tag': 'damikate'},
                                     {'start': 75, 'end': 88, 'tag': 'damianodavid'},
                                     {'start': 89, 'end': 100, 'tag': 'Eurovision'}], 'urls': [
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'},
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'}],
                        'mentions': [{'start': 3, 'end': 17, 'username': 'try'}]},
                                'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 1,
                                                   'quote_count': 0}, 'id': '1402600151789850626',
                                'author_id': '1400076690773135362', 'context_annotations': [{'domain': {'id': '118',
                                                                                                        'name': 'Award Show',
                                                                                                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                             'entity': {
                                                                                                 'id': '1376864097594011648',
                                                                                                 'name': 'Eurovision 2021'}}],
                                'text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmCgVjf'}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_possibly_sensitive(self):
        ent = {'hashtags': ['damikate', 'damianodavid', 'Eurovision'], 'mentions': ['try', 'marlenasslave'],
               'urls': ['https://t.co/wBDwmCgVjf', 'https://t.co/wBDwmCgVjf']}
        result = {'_id': '1402600531240046596',
                  'raw_text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate '
                              '#damianodavid #Eurovision https://t.co/wBDwmCgVjf',
                  'author_id': '957784397566050304',
                  'author_name': 'Milan ESC', 'author_username': 'milan_esc',
                  'created_at': '2021-06-09T12:16:40.000Z',
                  'possibly_sensitive': True,
                  'referenced_tweets': [{'id': '1402600151789850626', 'type': 'retweeted'}],
                  'complete_text': True,
                  'twitter_entities': ent, 'twitter_context_annotations': [{'domain': {'id': '118',
                                                                                       'name': 'Award Show',
                                                                                       'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                            'entity': {'id': '1376864097594011648',
                                                                                       'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'processed': False
                  }
        tweet = {'created_at': '2021-06-09T12:16:40.000Z', 'entities': {
            'hashtags': [{'start': 84, 'end': 93, 'tag': 'damikate'},
                         {'start': 94, 'end': 107, 'tag': 'damianodavid'},
                         {'start': 108, 'end': 119, 'tag': 'Eurovision'}],
            'mentions': [{'start': 3, 'end': 17, 'username': 'marlenasslave'}]},
                 'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                 'possibly_sensitive': True,
                 'id': '1402600531240046596', 'author_id': '957784397566050304',
                 'context_annotations': [{'domain': {
                     'id': '118', 'name': 'Award Show',
                     'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                     'entity': {
                         'id': '1376864097594011648',
                         'name': 'Eurovision 2021'}}],
                 'referenced_tweets': [{'type': 'retweeted', 'id': '1402600151789850626'}],
                 'text': 'RT @marlenasslave: [AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmC…'}
        includes = {'users': [{'id': '957784397566050304', 'name': 'Milan ESC', 'username': 'milan_esc'},
                              {'id': '1566112255', 'name': 'Miguel', 'username': 'teriz00'},
                              {'id': '1078462753461989378', 'name': 'juliå', 'username': 'athousandlivesz'}, ],
                    'tweets': [{'created_at': '2021-06-09T12:15:09.000Z', 'entities': {
                        'hashtags': [{'start': 65, 'end': 74, 'tag': 'damikate'},
                                     {'start': 75, 'end': 88, 'tag': 'damianodavid'},
                                     {'start': 89, 'end': 100, 'tag': 'Eurovision'}], 'urls': [
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'},
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'}],
                        'mentions': [{'start': 3, 'end': 17, 'username': 'try'}]},
                                'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 1,
                                                   'quote_count': 0}, 'id': '1402600151789850626',
                                'author_id': '1400076690773135362', 'context_annotations': [{'domain': {'id': '118',
                                                                                                        'name': 'Award Show',
                                                                                                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                             'entity': {
                                                                                                 'id': '1376864097594011648',
                                                                                                 'name': 'Eurovision 2021'}}],
                                'text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmCgVjf'}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))

    def test_user_location(self):
        ent = {'hashtags': ['damikate', 'damianodavid', 'Eurovision'], 'mentions': ['try', 'marlenasslave'],
               'urls': ['https://t.co/wBDwmCgVjf', 'https://t.co/wBDwmCgVjf']}
        result = {'_id': '1402600531240046596',
                  'raw_text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate '
                              '#damianodavid #Eurovision https://t.co/wBDwmCgVjf',
                  'author_id': '957784397566050304',
                  'author_name': 'Milan ESC', 'author_username': 'milan_esc',
                  'created_at': '2021-06-09T12:16:40.000Z',
                  'possibly_sensitive': True,
                  'referenced_tweets': [{'id': '1402600151789850626', 'type': 'retweeted'}],
                  'complete_text': True,
                  'twitter_entities': ent, 'twitter_context_annotations': [{'domain': {'id': '118',
                                                                                       'name': 'Award Show',
                                                                                       'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                            'entity': {'id': '1376864097594011648',
                                                                                       'name': 'Eurovision 2021'}}],
                  'metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                  'geo': {'user_location': 'Bari,Italia'},
                  'processed': False
                  }
        tweet = {'created_at': '2021-06-09T12:16:40.000Z', 'entities': {
            'hashtags': [{'start': 84, 'end': 93, 'tag': 'damikate'},
                         {'start': 94, 'end': 107, 'tag': 'damianodavid'},
                         {'start': 108, 'end': 119, 'tag': 'Eurovision'}],
            'mentions': [{'start': 3, 'end': 17, 'username': 'marlenasslave'}]},
                 'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
                 'possibly_sensitive': True,
                 'id': '1402600531240046596', 'author_id': '957784397566050304',
                 'context_annotations': [{'domain': {
                     'id': '118', 'name': 'Award Show',
                     'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                     'entity': {
                         'id': '1376864097594011648',
                         'name': 'Eurovision 2021'}}],
                 'referenced_tweets': [{'type': 'retweeted', 'id': '1402600151789850626'}],
                 'text': 'RT @marlenasslave: [AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmC…'}
        includes = {'users': [{'id': '957784397566050304', 'name': 'Milan ESC', 'username': 'milan_esc', "location": "Bari,Italia"},
                              {'id': '1566112255', 'name': 'Miguel', 'username': 'teriz00'},
                              {'id': '1078462753461989378', 'name': 'juliå', 'username': 'athousandlivesz'}, ],
                    'tweets': [{'created_at': '2021-06-09T12:15:09.000Z', 'entities': {
                        'hashtags': [{'start': 65, 'end': 74, 'tag': 'damikate'},
                                     {'start': 75, 'end': 88, 'tag': 'damianodavid'},
                                     {'start': 89, 'end': 100, 'tag': 'Eurovision'}], 'urls': [
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'},
                            {'start': 101, 'end': 124, 'url': 'https://t.co/wBDwmCgVjf',
                             'expanded_url': 'https://twitter.com/marlenasslave/status/1402600151789850626/photo/1',
                             'display_url': 'pic.twitter.com/wBDwmCgVjf'}],
                        'mentions': [{'start': 3, 'end': 17, 'username': 'try'}]},
                                'public_metrics': {'retweet_count': 1, 'reply_count': 0, 'like_count': 1,
                                                   'quote_count': 0}, 'id': '1402600151789850626',
                                'author_id': '1400076690773135362', 'context_annotations': [{'domain': {'id': '118',
                                                                                                        'name': 'Award Show',
                                                                                                        'description': 'Award shows, like the Oscars, Grammys, or VMAs'},
                                                                                             'entity': {
                                                                                                 'id': '1376864097594011648',
                                                                                                 'name': 'Eurovision 2021'}}],
                                'text': '[AU] В котором Катя и Дэвид поют «I wanna be your slave» дуэтом.\n#damikate #damianodavid #Eurovision https://t.co/wBDwmCgVjf'}]}
        self.maxDiff = None
        self.assertDictEqual(result, util.pre_process_response(tweet, includes))


if __name__ == "__main__":
    unittest.main()  # run all tests

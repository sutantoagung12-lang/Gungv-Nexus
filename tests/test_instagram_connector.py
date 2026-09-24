from integrations.instagram.connector import InstagramConfig, authorization_url


def test_authorization_url_contains_instagram_login_scopes():
    config = InstagramConfig("id", "secret", "https://example.com/callback", "v23.0")
    url, state = authorization_url(config, state="test-state")
    assert "instagram_business_basic" in url
    assert "instagram_business_content_publish" in url
    assert "enable_fb_login=0" in url
    assert state == "test-state"


def test_config_requires_api_version_only_for_graph_calls():
    config = InstagramConfig("id", "secret", "https://example.com/callback", "")
    assert config.client_id == "id"
    assert config.api_version == ""

CREATE OR REPLACE FUNCTION get_user_id_by_telegram_id(tg_id BIGINT)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN(
		SELECT id FROM users WHERE telegram_id = tg_id
	);
END;
$$;

CREATE OR REPLACE FUNCTION get_user_id_by_login_password(login_text TEXT, password_text TEXT)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN(
		SELECT id FROM users WHERE username = login_text and password_hash = password_text
	);
END;
$$;
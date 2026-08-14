const TOKEN_KEY = "hdfc_auth_token";
const USER_KEY = "hdfc_auth_user";
const RECENT_ACCOUNTS_KEY = "hdfc_recent_accounts";

export function saveAuth(accessToken, user) {
  localStorage.setItem(TOKEN_KEY, accessToken);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function getAuthToken() {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem(TOKEN_KEY);
}

export function getAuthUser() {
  if (typeof window === "undefined") {
    return null;
  }

  const value = localStorage.getItem(USER_KEY);

  if (!value) {
    return null;
  }

  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getRecentAccounts() {
  if (typeof window === "undefined") {
    return [];
  }

  try {
    const value = localStorage.getItem(
      RECENT_ACCOUNTS_KEY
    );

    return value ? JSON.parse(value) : [];
  } catch {
    return [];
  }
}

export function saveRecentAccount(user) {
  if (typeof window === "undefined") {
    return;
  }

  const existing = getRecentAccounts().filter(
    (account) =>
      account.email !== user.email
  );

  const updated = [
    {
      full_name: user.full_name,
      email: user.email,
    },
    ...existing,
  ].slice(0, 5);

  localStorage.setItem(
    RECENT_ACCOUNTS_KEY,
    JSON.stringify(updated)
  );
}

export function removeRecentAccount(email) {
  if (typeof window === "undefined") {
    return;
  }

  const updated = getRecentAccounts().filter(
    (account) =>
      account.email !== email
  );

  localStorage.setItem(
    RECENT_ACCOUNTS_KEY,
    JSON.stringify(updated)
  );
}
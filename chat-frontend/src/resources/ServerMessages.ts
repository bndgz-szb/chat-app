interface BaseMessage {
  type: string;
  message: string;
}

interface UserPresenceMessage {
  type: string;
  username: string;
}

export interface UnicastMessage extends BaseMessage {
  type: 'message';
  from: string;
  to: string;
}

export interface BroadcastMessage extends BaseMessage {
  type: 'broadcast';
  from: string;
}

export interface ErrorMessage extends BaseMessage {
  type: 'error';
}

export interface UserListMessage {
  type: 'user_list';
  users: string[];
}

export interface UserLoginMessage extends UserPresenceMessage {
  type: 'user_login';
}

export interface UserLogoutMessage extends UserPresenceMessage {
  type: 'user_logout';
}

export type ServerToClientMessage =
  | UnicastMessage
  | BroadcastMessage
  | ErrorMessage
  | UserListMessage
  | UserLoginMessage
  | UserLogoutMessage;

export type ChatMessage = UnicastMessage | BroadcastMessage;

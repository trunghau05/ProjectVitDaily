export interface NavItem {
  label: string;
  route: string;
  icon?: string;
  children?: NavItem[];
}

export const navItems: NavItem[] = [
  {
    label: 'Dashboards',
    route: 'dashboard',
    icon: 'dashboard',
  },
  {
    label: 'Cá nhân',
    route: 'person',
    icon: 'person',
    children: [
      { label: 'Ghi chú', route: 'note', icon: 'notes' },
      { label: 'Công việc', route: 'work', icon: 'work' },
    ],
  },
  {
    label: 'Nhóm',
    route: 'groups',
    icon: 'groups',
    children: [{ label: 'Cộng tác', route: 'workspace', icon: 'workspaces' }],
  },
  {
    label: 'Tài khoản',
    route: 'account',
    icon: 'account_circle',
  },
  {
    label: 'Cài đặt',
    route: 'settings',
    icon: 'settings',
  },
];

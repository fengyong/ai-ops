from django.contrib.auth.models import User

try:
    user = User.objects.get(username='testuser')
    print(f'用户存在: {user.username}')
    print(f'是否激活: {user.is_active}')
    print(f'是否是超级用户: {user.is_superuser}')
    
    # 验证密码
    if user.check_password('testpass123'):
        print('密码正确: testpass123')
    else:
        print('密码错误')
        
except User.DoesNotExist:
    print('用户不存在')

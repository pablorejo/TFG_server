# Build
```bash
docker-compose down
docker-compose up -d --build
```

# Scale
If you want scale inferency mortor to 5 new containers use it
```bash
docker-compose up -d --scale inferency_motor=5
```

# Stop
```bash
docker-compose down
```
set $i = 0
set $end = 65
set $current = *(uint64_t *)($rbp-0x78)
while ($i < $end)
    printf "%02x", *(uint8_t *)($current+0x10)
    set $current = *(uint64_t *)$current
    set $i = $i + 1
end
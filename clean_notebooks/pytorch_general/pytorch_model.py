from torch import nn, optim

def train_model(model: nn.Module, 
                log_dir: str,
                train_loader,
                criterion,
                optimizer,
                num_epochs,
               log_freq) -> nn.Module:
    now = time.mktime(datetime.datetime.now().timetuple()) - 1500000000
    logger = Logger(f'{log_dir} ({now})/')

    model = model.to(device)

    total_step = len(train_loader)
    for epoch in range(num_epochs):
        running_loss = 0
        for step, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.long().to(device)

            output = model(images).to(device)
            loss = criterion(output, labels).to(device)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Compute accuracy
            _, argmax = torch.max(output, 1)
            accuracy = (labels == argmax.squeeze()).float().mean()

            running_loss += loss.item()

            if step % log_freq == 0:
                overall_step = epoch*total_step + step

                # 1. Log scalar values (scalar summary)
                info = { 'loss': loss.item(), 'accuracy': accuracy.item() }

                for key, value in info.items():
                    logger.scalar_summary(key, value, overall_step)

                # 2. Log values and gradients of the parameters (histogram)
                for key, value in model.named_parameters():
                    key = key.replace('.', '/')
                    logger.histo_summary(key, value.data.cpu().numpy(), 
                                         overall_step)
                    logger.histo_summary(key+'/grad', 
                                         value.grad.data.cpu().numpy(), 
                                         overall_step)

        print(f"{epoch}: Training loss: {running_loss/len(train_loader)}")
        print(f"{epoch}: Training accuracy: {accuracy}")
    return model

def test_model(model, criterion, test_loader) -> float:
    model = model.to(device)
    correct = 0
    total = 0
    accuracies = []
    losses = []
    total_step = len(test_loader)
    with torch.no_grad():
        for i in range(total_step):
            for  images, labels in test_loader:
                images, labels = images.to(device), labels.long().to(device)

                output = model(images)
                loss = criterion(output, labels)
                losses.append(loss.item())


                # Compute accuracy
                _, argmax = torch.max(output, 1)
                accuracy = (labels == argmax.squeeze()).float().mean()
                accuracies.append(accuracy)

    print(f'Accuracy of the network on test images: '
          f'{np.average(accuracy.cpu())}')
    print(f'Avg. Loss of the network on test images: {np.average(losses)}')

    return np.average(accuracy.cpu())
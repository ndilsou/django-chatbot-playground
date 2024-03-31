/// <reference path="./.sst/platform/config.d.ts" />
import * as awsx from "@pulumi/awsx";
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const deploymentConfig = {
  ecsClusterName: "main",
  vpcId: "vpc-01a9910a9a06fbb57",
  albArn:
    "arn:aws:elasticloadbalancing:us-east-1:037131750441:loadbalancer/app/main/4ee6e23680a92a28",
  listernerArn:
    "arn:aws:elasticloadbalancing:us-east-1:037131750441:listener/app/main/4ee6e23680a92a28/0a43e282ef6c1bdf",
  containerImage: "my-repo/my-image:tag", // Replace with your image
  containerName: "main",
  containerPort: 80, // Replace with your container's port
};

export default $config({
  app(input) {
    return {
      name: "django-chatbot-playground",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
      providers: {
        aws: {
          region: "us-east-1",
          profile: "sandbox-sso",
        },
      },
    };
  },
  async run() {
    /* 1. we need to create an ecs service to deploy on our existing sandbox cluster.
    2. We need to connect the ecs service to our existing alb.
    */
    const fn = deployFunction();

    // // Get an existing ECS cluster by name
    // const cluster = aws.ecs.Cluster.get(
    //   "MainCluster",
    //   deploymentConfig.ecsClusterName
    // );

    // // Get an existing VPC by ID
    // const vpc = aws.ec2.Vpc.get("MainVpc", deploymentConfig.vpcId);

    // const alb = await aws.lb.getLoadBalancer({
    //   arn: deploymentConfig.albArn,
    // });
    // const albOutput = aws.alb.getLoadBalancerOutput({
    //   arn: deploymentConfig.albArn,
    // });
    // // const alb = new awsx.lb.ApplicationLoadBalancer("MainALB", {
    // //   name: "main",

    // // }, {impo})

    // // Create a new security group for the ECS service
    // const securityGroup = new aws.ec2.SecurityGroup("DjChatbotSecurityGroup", {
    //   vpcId: vpc.id,
    //   description: "Security group for ECS service",
    //   ingress: [
    //     {
    //       protocol: "tcp",
    //       fromPort: 80,
    //       toPort: 80,
    //       securityGroups: alb.securityGroups,
    //     },
    //     {
    //       protocol: "tcp",
    //       fromPort: 443,
    //       toPort: 443,
    //       securityGroups: alb.securityGroups,
    //     },
    //   ],
    //   egress: [
    //     {
    //       protocol: "-1",
    //       fromPort: 0,
    //       toPort: 0,
    //       cidrBlocks: ["0.0.0.0/0"],
    //     },
    //   ],
    // });

    // // const repo = new awsx.ecr.Repository("Repo", {
    // //   forceDelete: true,
    // // });

    // // const image = new awsx.ecr.Image("Image", {
    // //   repositoryUrl: repo.url,
    // //   context: ".",
    // //   dockerfile: "./Dockerfile",
    // //   platform: "linux/amd64",
    // // });
    // const targetGroup = new aws.lb.TargetGroup("DjChatbotTargetGroup", {
    //   port: 80,
    //   protocol: "HTTP",
    //   vpcId: vpc.id,
    // });

    // const listener = aws.lb.Listener.get(
    //   "DjChatbotListener",
    //   deploymentConfig.listernerArn
    // );

    // const listenerRule = new aws.lb.ListenerRule("DjChatbotListenerRule", {
    //   listenerArn: listener.arn,
    //   priority: 100,
    //   actions: [
    //     {
    //       type: "forward",
    //       targetGroupArn: targetGroup.arn,
    //     },
    //   ],
    //   conditions: [
    //     {
    //       hostHeader: {
    //         values: ["djchat.project-starter.voltor.be"],
    //       },
    //     },
    //   ],
    // });

    // // const listener = new aws.lb.Listener("DjChatbotListener", {
    // //   loadBalancerArn: alb.arn,
    // //   port: 80,
    // //   protocol: "HTTP",
    // //   defaultActions: [
    // //     {
    // //       type: "forward",
    // //       targetGroupArn: targetGroup.arn,
    // //     },
    // //   ],
    // // });

    // vpc.id.apply(async (id) => {
    //   const service = new awsx.ecs.FargateService("DjChatbotService", {
    //     cluster: cluster.arn,
    //     networkConfiguration: {
    //       subnets: await getPublicSubnets(id),
    //       securityGroups: [securityGroup.id],
    //     },
    //     desiredCount: 1,
    //     // loadBalancers: [
    //     //   {
    //     //     elbName: albOutput.name,
    //     //     containerName: "main",
    //     //     containerPort: 80,
    //     //   },
    //     // ],
    //     taskDefinitionArgs: {
    //       container: {
    //         name: "main",
    //         image: "nginx:latest",
    //         cpu: 128,
    //         memory: 512,
    //         essential: true,
    //         portMappings: [
    //           {
    //             targetGroup: targetGroup,
    //             containerPort: 80,
    //           },
    //         ],
    //       },
    //     },
    //   });
    // });
    // const url = pulumi.interpolate`http://${alb.dnsName}`;

    // return {
    //   url,
    // };
    // // // Create a task definition for the ECS service
    // // const taskDefinition = new aws.ecs.TaskDefinition("app-task", {
    // //   family: "dj-chatbot-playground",
    // //   cpu: "256",
    // //   memory: "512",
    // //   networkMode: "awsvpc",
    // //   requiresCompatibilities: ["FARGATE"],
    // //   // executionRoleArn: aws.iam.Role.get("ecsExecutionRole", "ecsExecutionRole")
    // //   //   .arn, // Use your existing execution role ARN
    // //   containerDefinitions: pulumi
    // //     .output([
    // //       {
    // //         name: deploymentConfig.containerName,
    // //         image: deploymentConfig.containerImage,
    // //         portMappings: [
    // //           {
    // //             containerPort: deploymentConfig.containerPort,
    // //             hostPort: deploymentConfig.containerPort,
    // //             protocol: "tcp",
    // //           },
    // //         ],
    // //       },
    // //     ])
    // //     .apply(JSON.stringify),
    // // });

    // // // Create an ECS service
    // // const service = new aws.ecs.Service(
    // //   "app-service",
    // //   {
    // //     cluster: cluster.arn,
    // //     desiredCount: 1,
    // //     launchType: "FARGATE",
    // //     taskDefinition: taskDefinition.arn,
    // //     networkConfiguration: {
    // //       subnets: await getPublicSubnets(vpc.id.get()), // Use your VPC's subnet IDs
    // //       securityGroups: [securityGroup.id],
    // //     },
    // //     loadBalancers: [
    // //       {
    // //         targetGroupArn: deploymentConfig.albArn, // Use your ALB's target group ARN
    // //         containerName: deploymentConfig.containerName,
    // //         containerPort: deploymentConfig.containerPort,
    // //       },
    // //     ],
    // //   },
    // //   { dependsOn: [securityGroup] }
    // // );
  },
});

async function getPublicSubnets(vpcId: string): Promise<string[]> {
  // Fetch all subnets that are associated with the given VPC and have the 'Type: public' tag
  const subnets = await aws.ec2.getSubnets({
    filters: [
      { name: "vpc-id", values: [vpcId] },
      { name: "tag:aws-cdk:subnet-type", values: ["Public"] },
    ],
    // vpcId: vpcId,
    // tags: {
    //   Type: "public",
    // },
  });

  return subnets.ids;
}

function deployFunction() {
  // const repo = new awsx.ecr.Repository("djchatbot-fn", {
  //   forceDelete: true,
  // });
  const repo = new aws.ecr.Repository("DjChatbotFn", {
    name: "djchatbot-fn",
    forceDelete: true,
  });

  console.log("CWD: ", __dirname);
  console.log("CWD: ", process.cwd());
  const image = new awsx.ecr.Image("DjChatFnImage", {
    repositoryUrl: repo.repositoryUrl,
    context: "../../../",
    dockerfile: "../../../lambda.Dockerfile",
    platform: "linux/amd64",
  });

  const role = new aws.iam.Role("DjChatFnRole", {
    assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
      Service: "lambda.amazonaws.com",
    }),
  });

  new aws.iam.RolePolicyAttachment("DjChatLambdaFullAccess", {
    role: role.name,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaExecute,
  });

  const fn = new aws.lambda.Function("DjChatFn", {
    packageType: "Image",
    imageUri: image.imageUri,
    role: role.arn,
    timeout: 900,
  });
  return fn;
}

async function deployApiService() {
  // Get an existing ECS cluster by name
  const cluster = aws.ecs.Cluster.get(
    "MainCluster",
    deploymentConfig.ecsClusterName
  );

  // Get an existing VPC by ID
  const vpc = aws.ec2.Vpc.get("MainVpc", deploymentConfig.vpcId);

  const alb = await aws.lb.getLoadBalancer({
    arn: deploymentConfig.albArn,
  });
  const albOutput = aws.alb.getLoadBalancerOutput({
    arn: deploymentConfig.albArn,
  });
  // const alb = new awsx.lb.ApplicationLoadBalancer("MainALB", {
  //   name: "main",

  // }, {impo})

  // Create a new security group for the ECS service
  const securityGroup = new aws.ec2.SecurityGroup("DjChatbotSecurityGroup", {
    vpcId: vpc.id,
    description: "Security group for ECS service",
    ingress: [
      {
        protocol: "tcp",
        fromPort: 80,
        toPort: 80,
        securityGroups: alb.securityGroups,
      },
      {
        protocol: "tcp",
        fromPort: 443,
        toPort: 443,
        securityGroups: alb.securityGroups,
      },
    ],
    egress: [
      {
        protocol: "-1",
        fromPort: 0,
        toPort: 0,
        cidrBlocks: ["0.0.0.0/0"],
      },
    ],
  });

  const repo = new awsx.ecr.Repository("DjChatbotApiRepo", {
    name: "djchatbot-api",
    forceDelete: true,
  });

  const image = new awsx.ecr.Image("DjChatbotApiImage", {
    repositoryUrl: repo.url,
    context: "../../../",
    dockerfile: "../../../Dockerfile",
    platform: "linux/amd64",
  });
  const targetGroup = new aws.lb.TargetGroup("DjChatbotApiTargetGroup", {
    port: 80,
    protocol: "HTTP",
    vpcId: vpc.id,
  });

  const listener = aws.lb.Listener.get(
    "DjChatbotListener",
    deploymentConfig.listernerArn
  );

  const listenerRule = new aws.lb.ListenerRule("DjChatbotApiListenerRule", {
    listenerArn: listener.arn,
    priority: 100,
    actions: [
      {
        type: "forward",
        targetGroupArn: targetGroup.arn,
      },
    ],
    conditions: [
      {
        hostHeader: {
          values: ["djchat.project-starter.voltor.be"],
        },
      },
    ],
  });

  // const listener = new aws.lb.Listener("DjChatbotListener", {
  //   loadBalancerArn: alb.arn,
  //   port: 80,
  //   protocol: "HTTP",
  //   defaultActions: [
  //     {
  //       type: "forward",
  //       targetGroupArn: targetGroup.arn,
  //     },
  //   ],
  // });

  vpc.id.apply(async (id) => {
    const service = new awsx.ecs.FargateService("DjChatbotApiService", {
      cluster: cluster.arn,
      networkConfiguration: {
        assignPublicIp: true,
        subnets: await getPublicSubnets(id),
        securityGroups: [securityGroup.id],
      },
      desiredCount: 1,
      name: "djchatbot-api",
      // capacityProviderStrategies: [
      //   {
      //     capacityProvider: "FARGATE_SPOT",
      //     weight: 1, // Use Fargate Spot for the entire capacity.
      //     base: 0, // No minimum number of tasks on Fargate Spot.
      //   },
      // ],
      taskDefinitionArgs: {
        container: {
          name: "main",
          image: "nginx:latest",
          cpu: 128,
          memory: 512,
          essential: true,
          portMappings: [
            {
              targetGroup: targetGroup,
              containerPort: 80,
            },
          ],
        },
      },
    });
  });
  const url = pulumi.interpolate`http://${alb.dnsName}`;

  return {
    url,
  };
  // // Create a task definition for the ECS service
  // const taskDefinition = new aws.ecs.TaskDefinition("app-task", {
  //   family: "dj-chatbot-playground",
  //   cpu: "256",
  //   memory: "512",
  //   networkMode: "awsvpc",
  //   requiresCompatibilities: ["FARGATE"],
  //   // executionRoleArn: aws.iam.Role.get("ecsExecutionRole", "ecsExecutionRole")
  //   //   .arn, // Use your existing execution role ARN
  //   containerDefinitions: pulumi
  //     .output([
  //       {
  //         name: deploymentConfig.containerName,
  //         image: deploymentConfig.containerImage,
  //         portMappings: [
  //           {
  //             containerPort: deploymentConfig.containerPort,
  //             hostPort: deploymentConfig.containerPort,
  //             protocol: "tcp",
  //           },
  //         ],
  //       },
  //     ])
  //     .apply(JSON.stringify),
  // });

  // // Create an ECS service
  // const service = new aws.ecs.Service(
  //   "app-service",
  //   {
  //     cluster: cluster.arn,
  //     desiredCount: 1,
  //     launchType: "FARGATE",
  //     taskDefinition: taskDefinition.arn,
  //     networkConfiguration: {
  //       subnets: await getPublicSubnets(vpc.id.get()), // Use your VPC's subnet IDs
  //       securityGroups: [securityGroup.id],
  //     },
  //     loadBalancers: [
  //       {
  //         targetGroupArn: deploymentConfig.albArn, // Use your ALB's target group ARN
  //         containerName: deploymentConfig.containerName,
  //         containerPort: deploymentConfig.containerPort,
  //       },
  //     ],
  //   },
  //   { dependsOn: [securityGroup] }
  // );
}
